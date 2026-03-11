"""
predict_cli.py — Contoh implementasi model intent (intent_model.pkl + vectorizer.pkl)
Jalankan: python predict_cli.py
"""

import os
import pickle
import sys


# ─── Warna terminal (ANSI) ───────────────────────────────────────────────────

RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
WHITE   = "\033[97m"


def clr(text, *codes):
    return "".join(codes) + str(text) + RESET


# ─── Load model ──────────────────────────────────────────────────────────────

MODEL_PATH      = "intent_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"


def load_model():
    missing = []
    if not os.path.exists(MODEL_PATH):
        missing.append(MODEL_PATH)
    if not os.path.exists(VECTORIZER_PATH):
        missing.append(VECTORIZER_PATH)

    if missing:
        print(clr("\n  ✗ File model tidak ditemukan:", RED, BOLD))
        for f in missing:
            print(clr(f"    • {f}", RED))
        print(clr(
            "\n  Latih model terlebih dahulu melalui aplikasi utama:\n"
            "    1. Jalankan  : python app.py\n"
            "    2. Buka      : http://localhost:5000\n"
            "    3. Navigasi ke halaman ⚡ Latih Model → klik Mulai Training\n",
            YELLOW
        ))
        sys.exit(1)

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    return model, vectorizer


# ─── Prediksi ────────────────────────────────────────────────────────────────

def predict(text: str, model, vectorizer) -> dict:
    X          = vectorizer.transform([text])
    intent     = model.predict(X)[0]
    proba      = model.predict_proba(X)[0]
    classes    = model.classes_
    confidence = float(max(proba))

    # Top-3 kandidat
    top3 = sorted(zip(classes, proba), key=lambda x: x[1], reverse=True)[:3]

    return {
        "intent":     intent,
        "confidence": round(confidence * 100, 2),
        "top3":       [(c, round(p * 100, 2)) for c, p in top3],
    }


# ─── Tampilan bar confidence ─────────────────────────────────────────────────

def confidence_bar(pct: float, width: int = 30) -> str:
    filled = int(pct / 100 * width)
    bar    = "█" * filled + "░" * (width - filled)
    if pct >= 75:
        color = GREEN
    elif pct >= 50:
        color = YELLOW
    else:
        color = RED
    return clr(bar, color) + clr(f"  {pct:.1f}%", BOLD, WHITE)


# ─── Banner ──────────────────────────────────────────────────────────────────

BANNER = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
║          🧠  Intent Prediction CLI                   ║
║          Model: TF-IDF + Logistic Regression         ║
╚══════════════════════════════════════════════════════╝{RESET}
"""

HELP_TEXT = clr(
    "  Perintah khusus:\n"
    "    exit / quit / q  →  Keluar dari program\n"
    "    help             →  Tampilkan bantuan ini\n"
    "    clear            →  Bersihkan layar\n",
    DIM
)


# ─── Main loop ───────────────────────────────────────────────────────────────

def main():
    print(BANNER)
    print(clr("  Memuat model...", DIM), end=" ", flush=True)
    model, vectorizer = load_model()

    n_classes = len(model.classes_)
    print(clr(f"✓  ({n_classes} intent dimuat)\n", GREEN, BOLD))
    print(HELP_TEXT)

    separator = clr("  " + "─" * 52, DIM)

    while True:
        try:
            raw = input(clr("  ➤ Masukkan teks: ", CYAN, BOLD))
        except (KeyboardInterrupt, EOFError):
            print(clr("\n\n  Sampai jumpa! 👋\n", YELLOW))
            break

        text = raw.strip()

        # Perintah khusus
        if not text:
            continue
        if text.lower() in ("exit", "quit", "q"):
            print(clr("\n  Sampai jumpa! 👋\n", YELLOW))
            break
        if text.lower() == "help":
            print(HELP_TEXT)
            continue
        if text.lower() == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            print(BANNER)
            continue

        # Prediksi
        result = predict(text, model, vectorizer)

        print(separator)
        print(clr(f"\n  📝 Teks     : ", DIM) + clr(f'"{text}"', WHITE, BOLD))
        print()
        print(clr("  🎯 Intent   : ", DIM) + clr(f" {result['intent']} ", MAGENTA, BOLD))
        print()
        print(clr("  📊 Confidence:", DIM))
        print(f"     {confidence_bar(result['confidence'])}")
        print()

        # Top-3 kandidat
        print(clr("  🏆 Top-3 Kandidat:", DIM))
        for i, (cls, pct) in enumerate(result["top3"], 1):
            marker = clr("▶", GREEN, BOLD) if i == 1 else clr(" ", DIM)
            label  = clr(cls, WHITE, BOLD) if i == 1 else clr(cls, DIM)
            bar_w  = 20
            filled = int(pct / 100 * bar_w)
            mini   = clr("█" * filled + "░" * (bar_w - filled), BLUE if i > 1 else GREEN)
            print(f"     {marker} {label:<35} {mini}  {clr(f'{pct:.1f}%', DIM)}")

        print(f"\n{separator}\n")


if __name__ == "__main__":
    main()