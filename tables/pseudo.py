# ============================================================
# pseudo.py - Pseudo-Komut Donusturucusu (Bonus)
# ============================================================
# Kullanici dostu pseudo-komutlari gercek RV32I komutlarina
# donusturur. Encoder'dan ONCE calistirilir.
#
# Desteklenen pseudo-komutlar:
#   li rd, imm  -> addi rd, x0, imm  (kucuk) veya lui+addi (buyuk)
#   mv rd, rs   -> addi rd, rs, 0
#   j label     -> jal x0, label
#   nop         -> addi x0, x0, 0
#   ret         -> jalr x0, ra, 0
#   not rd, rs  -> xori rd, rs, -1
#   neg rd, rs  -> sub rd, x0, rs
# ============================================================


def is_pseudo(mnemonic):
    """Verilen komut bir pseudo-komut mu?"""
    return mnemonic.upper() in ["LI", "MV", "J", "NOP", "RET", "NOT", "NEG"]


def expand_pseudo(token):
    """Pseudo-komutu gercek RV32I komut(lar)ina donusturur.

    Args:
        token: Lexer ciktisi {"line_num", "label", "mnemonic", "operands", ...}

    Returns:
        Gercek komut token listesi (1 veya 2 eleman)
        Ornek: li x1, 0x12345 -> [lui_token, addi_token]
    """
    mnemonic = token["mnemonic"].upper()
    operands = token["operands"]
    line_num = token["line_num"]

    # Genisletilmis komutlar - her biri ayni formatta token
    expanded = []

    if mnemonic == "NOP":
        # nop -> addi x0, x0, 0
        expanded.append(_make_token(line_num, token["label"], "ADDI", ["x0", "x0", "0"]))

    elif mnemonic == "MV":
        # mv rd, rs -> addi rd, rs, 0
        if len(operands) >= 2:
            expanded.append(_make_token(line_num, token["label"], "ADDI",
                                        [operands[0], operands[1], "0"]))

    elif mnemonic == "J":
        # j label -> jal x0, label
        if len(operands) >= 1:
            expanded.append(_make_token(line_num, token["label"], "JAL",
                                        ["x0", operands[0]]))

    elif mnemonic == "RET":
        # ret -> jalr x0, ra, 0
        expanded.append(_make_token(line_num, token["label"], "JALR",
                                    ["x0", "ra", "0"]))

    elif mnemonic == "NOT":
        # not rd, rs -> xori rd, rs, -1
        if len(operands) >= 2:
            expanded.append(_make_token(line_num, token["label"], "XORI",
                                        [operands[0], operands[1], "-1"]))

    elif mnemonic == "NEG":
        # neg rd, rs -> sub rd, x0, rs
        if len(operands) >= 2:
            expanded.append(_make_token(line_num, token["label"], "SUB",
                                        [operands[0], "x0", operands[1]]))

    elif mnemonic == "LI":
        # li rd, imm -> immediate degerine gore 1 veya 2 komut
        if len(operands) >= 2:
            expanded = _expand_li(token)

    return expanded


def _expand_li(token):
    """LI pseudo-komutunu genisletir.

    Kucuk immediate (-2048..2047): sadece addi rd, x0, imm
    Buyuk immediate: lui rd, upper + addi rd, rd, lower

    DIKKAT: Sign-extension duzeltmesi gerekli!
    Eger lower 12-bit'in en ust biti (bit 11) set ise,
    addi isleminde sign-extension olacagi icin lui degerine +1 eklenmelidir.
    """
    rd = token["operands"][0]
    imm_str = token["operands"][1]
    line_num = token["line_num"]

    # Immediate degeri parse et
    try:
        if imm_str.startswith("0x") or imm_str.startswith("0X"):
            imm = int(imm_str, 16)
        elif imm_str.startswith("0b") or imm_str.startswith("0B"):
            imm = int(imm_str, 2)
        else:
            imm = int(imm_str)
    except ValueError:
        # Parse edemedi - hata main.py'de yakalanacak
        return [_make_token(line_num, token["label"], "ADDI", [rd, "x0", imm_str])]

    # 32-bit'e sigdir
    imm = imm & 0xFFFFFFFF

    # Signed 32-bit olarak kontrol et
    if imm & 0x80000000:
        imm_signed = imm - 0x100000000
    else:
        imm_signed = imm

    # 12-bit'e sigiyor mu? (-2048 .. 2047)
    if -2048 <= imm_signed <= 2047:
        # Tek addi yeterli
        return [_make_token(line_num, token["label"], "ADDI",
                            [rd, "x0", str(imm_signed)])]

    # Buyuk immediate: lui + addi gerekli
    # Alt 12 bit (sign-extended)
    lower = imm_signed & 0xFFF
    if lower & 0x800:
        # Sign extension duzeltmesi: alt 12 bit negatif olacak
        # bu yuzden ust kisma +1 ekle
        lower = lower - 0x1000  # Signed lower
        upper = ((imm_signed - lower) >> 12) & 0xFFFFF
    else:
        upper = (imm_signed >> 12) & 0xFFFFF

    expanded = []

    # lui rd, upper
    expanded.append(_make_token(line_num, token["label"], "LUI",
                                [rd, str(upper)]))

    # addi rd, rd, lower
    expanded.append(_make_token(line_num, None, "ADDI",
                                [rd, rd, str(lower)]))

    return expanded


def _make_token(line_num, label, mnemonic, operands):
    """Yeni bir token olusturur (genisletilmis komut icin)."""
    return {
        "line_num": line_num,
        "label": label,
        "mnemonic": mnemonic,
        "operands": operands,
        "original": f"  [expanded] {mnemonic} {', '.join(operands)}"
    }
