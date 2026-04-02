# ============================================================
# directive.py - Direktif Islemcisi
# ============================================================
# .data, .text, .word, .byte, .org, .end direktiflerini isler.
# Program sayacini (PC) gunceller ve veri bolumune
# degerler yerlestirir.
# ============================================================

from assembler.parser import parse_immediate


def process_directive(token, current_pc, data_memory, error_handler):
    """Direktifi isler ve guncellenmis PC degerini dondurur.

    Args:
        token: Lexer ciktisi (mnemonic + operands)
        current_pc: Suanki program sayaci
        data_memory: Veri bellegi dict'i {adres: deger}
        error_handler: Hata yoneticisi

    Returns:
        Yeni PC degeri
    """
    directive = token["mnemonic"].lower()
    operands = token["operands"]
    line_num = token["line_num"]

    if directive == ".text":
        # Kod bolumune gec - PC degismez
        return current_pc

    elif directive == ".data":
        # Veri bolumune gec - PC degismez
        return current_pc

    elif directive == ".word":
        # 4 byte'lik veri yerlestirir
        if len(operands) == 0:
            error_handler.add_error(line_num, "directive",
                                    ".word direktifi bir deger gerektirir")
            return current_pc

        value = parse_immediate(operands[0])
        if value is None:
            error_handler.add_error(line_num, "directive",
                                    f".word icin gecersiz deger: '{operands[0]}'")
            return current_pc

        # 4 byte olarak bellege yaz
        data_memory[current_pc] = value & 0xFFFFFFFF
        return current_pc + 4

    elif directive == ".byte":
        # 1 byte'lik veri yerlestirir
        if len(operands) == 0:
            error_handler.add_error(line_num, "directive",
                                    ".byte direktifi bir deger gerektirir")
            return current_pc

        value = parse_immediate(operands[0])
        if value is None:
            error_handler.add_error(line_num, "directive",
                                    f".byte icin gecersiz deger: '{operands[0]}'")
            return current_pc

        data_memory[current_pc] = value & 0xFF
        return current_pc + 1

    elif directive == ".org":
        # Program sayacini belirtilen adrese atar
        if len(operands) == 0:
            error_handler.add_error(line_num, "directive",
                                    ".org direktifi bir adres gerektirir")
            return current_pc

        address = parse_immediate(operands[0])
        if address is None:
            error_handler.add_error(line_num, "directive",
                                    f".org icin gecersiz adres: '{operands[0]}'")
            return current_pc

        return address

    elif directive == ".end":
        # Dosya sonu - ozel bir isleme gerek yok
        return current_pc

    else:
        error_handler.add_error(line_num, "directive",
                                f"Bilinmeyen direktif: '{directive}'")
        return current_pc


def is_directive(mnemonic):
    """Verilen string bir direktif mi kontrol eder."""
    return mnemonic.lower() in [".data", ".text", ".word", ".byte", ".org", ".end"]
