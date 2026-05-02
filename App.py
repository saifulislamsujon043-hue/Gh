"""
NSFW Group Moderator Bot
========================
- Group e unsafe image ashle DELETE kore dibe
- Warn system + auto-mute
- Private chat e image scan
- Fully local NudeNet, no API key

Install:
    pip install "python-telegram-bot==21.6" "nudenet==3.4.2" pillow httpx

Run:
    python bot.py
"""

# ════════════════════════════════════════════════
#  CONFIG
# ════════════════════════════════════════════════
BOT_TOKEN         = "8227868963:AAFp14683OEhcrEDIs1BvGvO_8S_JhrGa6w"
ADMIN_IDS         = [6572397779]
DEFAULT_THRESHOLD = 0.55
WARN_LIMIT        = 3
MUTE_DURATION     = 600        # seconds (10 min)
MAX_WORKERS       = 6
SCAN_MAX_SIZE     = 320        # resize before scan for speed
# ════════════════════════════════════════════════

import io
import os
import asyncio
import logging
import tempfile
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

import httpx
from PIL import Image
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from telegram.error import TelegramError

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# ── NudeNet labels ────────────────────────────────────────────────────────────
UNSAFE_LABELS = {
    "FEMALE_GENITALIA_EXPOSED", "MALE_GENITALIA_EXPOSED",
    "FEMALE_BREAST_EXPOSED", "ANUS_EXPOSED", "BUTTOCKS_EXPOSED",
}
SUGGESTIVE_LABELS = {
    "FEMALE_BREAST_COVERED", "FEMALE_GENITALIA_COVERED",
    "MALE_GENITALIA_COVERED", "ANUS_COVERED", "BUTTOCKS_COVERED",
    "BELLY_EXPOSED", "ARMPITS_EXPOSED",
}

# ── State ─────────────────────────────────────────────────────────────────────
user_thresholds : dict[int, float]          = {}
user_stats      : dict[int, dict]           = {}
group_warns     : dict[int, dict[int, int]] = {}

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
detector = None
http     = None


# ════════════════════════════════════════════════
#  Detection
# ════════════════════════════════════════════════

def _resize_bytes(data: bytes) -> bytes:
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    if max(w, h) > SCAN_MAX_SIZE:
        ratio = SCAN_MAX_SIZE / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.BILINEAR)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


def _detect_sync(data: bytes) -> list:
    small = _resize_bytes(data)
    fd, path = tempfile.mkstemp(suffix=".jpg")
    try:
        os.write(fd, small)
        os.close(fd)
        return detector.detect(path)
    finally:
        try:
            os.unlink(path)
        except Exception:
            pass


async def detect_bytes(data: bytes) -> list:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, _detect_sync, data)


def classify(detections: list, threshold: float):
    hits = [
        (d["class"], round(d["score"], 3))
        for d in detections if d["score"] >= threshold
    ]
    unsafe     = [(l, s) for l, s in hits if l in UNSAFE_LABELS]
    suggestive = [(l, s) for l, s in hits if l in SUGGESTIVE_LABELS]
    if unsafe:
        return "UNSAFE", unsafe + suggestive
    elif suggestive:
        return "SUGGESTIVE", suggestive
    return "SAFE", hits


# ════════════════════════════════════════════════
#  Download
# ════════════════════════════════════════════════

async def download_bytes(bot, file_id: str) -> bytes:
    tg_file  = await bot.get_file(file_id)
    response = await http.get(tg_file.file_path)
    response.raise_for_status()
    return response.content


# ════════════════════════════════════════════════
#  State helpers
# ════════════════════════════════════════════════

def get_threshold(uid: int) -> float:
    return user_thresholds.get(uid, DEFAULT_THRESHOLD)


def bump_stats(uid: int, verdict: str):
    s = user_stats.setdefault(uid, {"total": 0, "safe": 0, "suggestive": 0, "unsafe": 0})
    s["total"] += 1
    s[verdict.lower()] = s.get(verdict.lower(), 0) + 1


def add_warn(chat_id: int, uid: int) -> int:
    g = group_warns.setdefault(chat_id, {})
    g[uid] = g.get(uid, 0) + 1
    return g[uid]


def reset_warns(chat_id: int, uid: int):
    group_warns.get(chat_id, {}).pop(uid, None)


def get_warns(chat_id: int, uid: int) -> int:
    return group_warns.get(chat_id, {}).get(uid, 0)


def is_group(update: Update) -> bool:
    return update.effective_chat.type in ("group", "supergroup")


def safe_name(user) -> str:
    """Return user full name, strip any special chars that break messages."""
    return (user.full_name or "User").replace("<", "").replace(">", "").replace("&", "")


def build_private_result(verdict: str, hits: list, threshold: float) -> str:
    EMOJI = {"UNSAFE": "UNSAFE", "SUGGESTIVE": "SUGGESTIVE", "SAFE": "SAFE"}
    ICON  = {"UNSAFE": "🔴", "SUGGESTIVE": "🟡", "SAFE": "🟢"}
    lines = [
        f"{ICON[verdict]} {EMOJI[verdict]}",
        "=" * 28,
        f"Threshold : {threshold}",
        f"Time      : {datetime.now().strftime('%H:%M:%S')}",
    ]
    if hits:
        lines += ["", "Detected:"]
        for label, score in hits:
            bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            tag = "🔴" if label in UNSAFE_LABELS else "🟡"
            lines.append(f"  {tag} {bar} {score:.3f}  {label}")
    else:
        lines += ["", "No flagged content found."]
    return "\n".join(lines)


def threshold_keyboard(uid: int) -> InlineKeyboardMarkup:
    current = get_threshold(uid)
    options = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    rows, row = [], []
    for v in options:
        row.append(InlineKeyboardButton(
            f"✅ {v}" if v == current else str(v),
            callback_data=f"thr_{v}"
        ))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


# ════════════════════════════════════════════════
#  Group moderation
# ════════════════════════════════════════════════

async def moderate_group(update: Update, ctx: ContextTypes.DEFAULT_TYPE, data: bytes):
    msg     = update.message
    chat_id = msg.chat_id
    user    = msg.from_user
    name    = safe_name(user)

    try:
        detections    = await detect_bytes(data)
        verdict, hits = classify(detections, DEFAULT_THRESHOLD)
    except Exception:
        log.exception("Detection error")
        return

    log.info(f"[GROUP {chat_id}] user={user.id} name={name} verdict={verdict}")

    if verdict != "UNSAFE":
        return

    warn_count = add_warn(chat_id, user.id)

    async def do_delete():
        try:
            await msg.delete()
        except TelegramError as e:
            log.warning(f"Delete failed: {e}")
            try:
                await ctx.bot.send_message(
                    chat_id,
                    "Give me Delete Messages permission to remove NSFW content automatically."
                )
            except Exception:
                pass

    async def do_warn_msg():
        if warn_count >= WARN_LIMIT:
            until = datetime.now() + timedelta(seconds=MUTE_DURATION)
            try:
                await ctx.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until,
                )
                extra = f"Muted for {MUTE_DURATION // 60} minutes."
            except TelegramError:
                extra = "Could not mute (need Restrict Members permission)."
            reset_warns(chat_id, user.id)
            text = (
                f"🚫 NSFW image deleted\n"
                f"User: {name}\n"
                f"Warns: {WARN_LIMIT}/{WARN_LIMIT}\n"
                f"{extra}"
            )
        else:
            text = (
                f"🚫 NSFW image deleted\n"
                f"User: {name}\n"
                f"Warning {warn_count}/{WARN_LIMIT} "
                f"({WARN_LIMIT - warn_count} more before mute)"
            )
        try:
            await ctx.bot.send_message(chat_id, text)
        except Exception:
            pass

    async def do_admin_notify():
        top  = hits[0] if hits else None
        text = (
            f"NSFW Alert\n"
            f"Group : {chat_id}\n"
            f"User  : {name} ({user.id})\n"
            f"Warn  : {warn_count}/{WARN_LIMIT}"
        )
        if top:
            text += f"\nLabel : {top[0]} ({top[1]:.2f})"
        for aid in ADMIN_IDS:
            try:
                await ctx.bot.send_message(aid, text)
            except Exception:
                pass

    await asyncio.gather(do_delete(), do_warn_msg(), do_admin_notify())


# ════════════════════════════════════════════════
#  Message handlers
# ════════════════════════════════════════════════

async def handle_photo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        data = await download_bytes(ctx.bot, update.message.photo[-1].file_id)
    except Exception as e:
        log.warning(f"Photo download error: {e}")
        return

    if is_group(update):
        await moderate_group(update, ctx, data)
        return

    uid       = update.effective_user.id
    threshold = get_threshold(uid)
    status    = await update.message.reply_text("Scanning...")
    try:
        verdict, hits = classify(await detect_bytes(data), threshold)
        bump_stats(uid, verdict)
        await update.message.reply_text(build_private_result(verdict, hits, threshold))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        await status.delete()


async def handle_document(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    ext = (doc.file_name or "").rsplit(".", 1)[-1].lower()
    if ext not in {"jpg", "jpeg", "png", "webp", "bmp", "tiff"}:
        if not is_group(update):
            await update.message.reply_text(f"Unsupported format: .{ext}")
        return

    try:
        data = await download_bytes(ctx.bot, doc.file_id)
    except Exception as e:
        log.warning(f"Doc download error: {e}")
        return

    if is_group(update):
        await moderate_group(update, ctx, data)
        return

    uid       = update.effective_user.id
    threshold = get_threshold(uid)
    status    = await update.message.reply_text("Scanning...")
    try:
        verdict, hits = classify(await detect_bytes(data), threshold)
        bump_stats(uid, verdict)
        await update.message.reply_text(build_private_result(verdict, hits, threshold))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        await status.delete()


# ════════════════════════════════════════════════
#  Commands  (all plain text, zero parse_mode)
# ════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if is_group(update):
        await update.message.reply_text(
            "NSFW Moderator is active.\n\n"
            "Unsafe images will be deleted automatically.\n\n"
            "Required bot permissions:\n"
            "  - Delete Messages\n"
            "  - Restrict Members\n\n"
            f"Warn limit: {WARN_LIMIT} strikes then mute ({MUTE_DURATION // 60} min)"
        )
    else:
        await update.message.reply_text(
            "NSFW Image Reviewer\n\n"
            "Send any photo or image file to scan it.\n\n"
            "Commands:\n"
            "  /threshold - adjust sensitivity\n"
            "  /mystats   - your scan history\n"
            "  /help      - more info"
        )


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if is_group(update):
        await update.message.reply_text(
            "Group Moderation\n\n"
            "Every image is scanned automatically.\n"
            f"UNSAFE image = deleted + warn.\n"
            f"{WARN_LIMIT} warns = muted for {MUTE_DURATION // 60} min.\n\n"
            "Admin commands:\n"
            "  /warns      - check warns (reply to user)\n"
            "  /resetwarn  - clear warns (reply to user)\n"
            "  /stats_all  - global stats"
        )
    else:
        await update.message.reply_text(
            "Send any photo or image file to get a verdict.\n\n"
            "  /threshold - pick sensitivity (0.3 to 0.8)\n\n"
            "Verdicts:\n"
            "  SAFE        - clean image\n"
            "  SUGGESTIVE  - partial content detected\n"
            "  UNSAFE      - explicit content detected\n\n"
            "Images are never saved to disk."
        )


async def cmd_threshold(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if is_group(update):
        return
    uid = update.effective_user.id
    await update.message.reply_text(
        f"Detection Threshold\n\nCurrent: {get_threshold(uid)}\n\nPick a new value:",
        reply_markup=threshold_keyboard(uid),
    )


async def cb_threshold(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cq  = update.callback_query
    uid = cq.from_user.id
    val = float(cq.data.split("_")[1])
    user_thresholds[uid] = val
    await cq.answer(f"Set to {val}")
    await cq.message.edit_text(
        f"Detection Threshold\n\nCurrent: {val}\n\nPick a new value:",
        reply_markup=threshold_keyboard(uid),
    )


async def cmd_mystats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    s   = user_stats.get(uid)
    if not s or not s["total"]:
        await update.message.reply_text("No scans yet.")
        return
    await update.message.reply_text(
        f"Your Scan Stats\n\n"
        f"Total       : {s['total']}\n"
        f"Safe        : {s.get('safe', 0)}\n"
        f"Suggestive  : {s.get('suggestive', 0)}\n"
        f"Unsafe      : {s.get('unsafe', 0)}\n\n"
        f"Threshold   : {get_threshold(uid)}"
    )


async def cmd_stats_all(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not user_stats:
        await update.message.reply_text("No data yet.")
        return
    tu = len(user_stats)
    ts = sum(s["total"]            for s in user_stats.values())
    tf = sum(s.get("unsafe", 0)    for s in user_stats.values())
    tg = sum(s.get("suggestive", 0)for s in user_stats.values())
    tk = sum(s.get("safe", 0)      for s in user_stats.values())
    await update.message.reply_text(
        f"Global Stats\n\n"
        f"Users       : {tu}\n"
        f"Total scans : {ts}\n"
        f"Safe        : {tk}\n"
        f"Suggestive  : {tg}\n"
        f"Unsafe      : {tf}"
    )


async def cmd_warns(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_group(update):
        return
    msg = update.message
    if not msg.reply_to_message:
        await msg.reply_text("Reply to a user message to check their warns.")
        return
    target = msg.reply_to_message.from_user
    count  = get_warns(msg.chat_id, target.id)
    await msg.reply_text(f"{safe_name(target)}: {count}/{WARN_LIMIT} warns")


async def cmd_resetwarn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_group(update):
        return
    msg = update.message
    if update.effective_user.id not in ADMIN_IDS:
        m = await ctx.bot.get_chat_member(msg.chat_id, update.effective_user.id)
        if m.status not in ("administrator", "creator"):
            return
    if not msg.reply_to_message:
        await msg.reply_text("Reply to a user message to reset their warns.")
        return
    target = msg.reply_to_message.from_user
    reset_warns(msg.chat_id, target.id)
    await msg.reply_text(f"Warns cleared for {safe_name(target)}.")


async def cmd_broadcast(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a message to broadcast it.")
        return
    sent = fail = 0
    for uid in list(user_stats.keys()):
        try:
            await update.message.reply_to_message.copy(chat_id=uid)
            sent += 1
        except Exception:
            fail += 1
    await update.message.reply_text(f"Broadcast done. Sent: {sent}  Failed: {fail}")


# ════════════════════════════════════════════════
#  Startup / Shutdown
# ════════════════════════════════════════════════

async def on_startup(app):
    global http
    http = httpx.AsyncClient(
        timeout=15,
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
    )
    log.info("httpx client ready.")


async def on_shutdown(app):
    await http.aclose()
    executor.shutdown(wait=False)
    log.info("Shutdown complete.")


# ════════════════════════════════════════════════
#  Entry point
# ════════════════════════════════════════════════

def main():
    global detector
    from nudenet import NudeDetector
    log.info("Loading NudeNet...")
    detector = NudeDetector()
    log.info("NudeNet ready.")

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)
        .post_init(on_startup)
        .post_shutdown(on_shutdown)
        .build()
    )

    app.add_handler(CommandHandler("start",     cmd_start))
    app.add_handler(CommandHandler("help",      cmd_help))
    app.add_handler(CommandHandler("threshold", cmd_threshold))
    app.add_handler(CommandHandler("mystats",   cmd_mystats))
    app.add_handler(CommandHandler("stats_all", cmd_stats_all))
    app.add_handler(CommandHandler("warns",     cmd_warns))
    app.add_handler(CommandHandler("resetwarn", cmd_resetwarn))
    app.add_handler(CommandHandler("broadcast", cmd_broadcast))
    app.add_handler(CallbackQueryHandler(cb_threshold, pattern=r"^thr_"))
    app.add_handler(MessageHandler(filters.PHOTO,          handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, handle_document))

    log.info("Bot running.")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
