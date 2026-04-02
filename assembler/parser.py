# ============================================================
# parser.py - Yapisal Ayristirma (Parser)
# ============================================================
# Lexer ciktisini alarak her satirin turunu belirler ve
# operandlari yapisal olarak ayristirir.
# Ozellikle S-Type (store) komutlarinda offset(register)
# formatini parcalar: "0(x2)" -> offset=0, register="x2"
# ============================================================

from tables.opcode_table import get_instruction_info, get_register_number


# Desteklenen direktifler
DIRECTIVES = [".data", ".text", ".word", ".byte", ".org", ".end"]

# Pseudo-komut listesi (bonus)
PSEUDO_INSTRUCTIONS = ["LI", "MV", "J", "NOP", "RET", "NOT", "NEG"]


def classify_line(token):
    """Satirin turunu belirler.

    Returns: "instruction", "directive", "label_only", "pseudo"
    """
    # Sadece label olan satir
    if token["mnemonic"] is None:
        return "label_only"

    mnemonic = token["mnemonic"]

    # Direktif kontrolu (. ile baslar)
    if mnemonic.startswith('.'):
        return "directive"

    # Pseudo-komut kontrolu
    if mnemonic.upper() in PSEUDO_INSTRUCTIONS:
        return "pseudo"

    # Normal instruction
    if get_instruction_info(mnemonic) is not None:
        return "instruction"

    # Bilinmeyen komut
    return "unknown"


def parse_immediate(value_str):
    """Immediate (sabit) degeri parse eder.

    Desteklenen formatlar:
        - Decimal: 100, -50
        - Hexadecimal: 0x1A, 0xFF
        - Binary: 0b1010
    """
    value_str = value_str.strip()
    try:
        if value_str.startswith("0x") or value_str.startswith("0X"):
            return int(value_str, 16)
        elif value_str.startswith("0b") or value_str.startswith("0B"):
            return int(value_str, 2)
        else:
            return int(value_str)
    except ValueError:
        return None  # Parse edemedi - belki label'dir


def parse_memory_operand(operand):
    """S-Type ve Load komutlari icin offset(register) formatini parcalar.

    Ornek: "0(x2)" -> {"offset": 0, "register": "x2"}
    Ornek: "-4(sp)" -> {"offset": -4, "register": "sp"}
    """
    operand = operand.strip()

    # Parantez kontrolu
    if '(' not in operand or ')' not in operand:
        return None

    # offset ve register'i ayir
    paren_start = operand.index('(')
    paren_end = operand.index(')')

    offset_str = operand[:paren_start].strip()
    register_str = operand[paren_start + 1:paren_end].strip()

    # Offset degerini parse et
    if offset_str == '':
        offset = 0
    else:
        offset = parse_immediate(offset_str)
        if offset is None:
            return None

    return {"offset": offset, "register": register_str}


def validate_register(name, error_handler, line_num):
    """Register adinin gecerli olup olmadigini kontrol eder.

    Gecerliyse register numarasini dondurur, degilse hata ekler.
    """
    reg_num = get_register_number(name)
    if reg_num is None:
        error_handler.add_error(line_num, "syntax",
                                f"Gecersiz register adi: '{name}'")
        return None
    return reg_num
