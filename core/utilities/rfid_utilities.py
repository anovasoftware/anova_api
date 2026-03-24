import re


def normalize_rfid(uid: str) -> str:
    if not uid:
        return ''

    uid = uid.strip().upper()

    if not re.fullmatch(r'[0-9A-F]+', uid):
        raise ValueError(f'Invalid RFID code (non-hex characters): {uid}')

    # Their raw format:
    # 88 + 7-byte UID in alternate byte order
    if len(uid) == 16 and uid.startswith('88'):
        uid7 = uid[2:]          # remove cascade tag, now 14 chars
        manuf = uid7[:2]        # e.g. 04
        rest = uid7[2:]         # remaining 6 bytes
        byte_pairs = [rest[i:i+2] for i in range(0, len(rest), 2)]
        return manuf + ''.join(reversed(byte_pairs))

    # Your canonical format:
    # already normalized
    if len(uid) == 14:
        return uid

    raise ValueError(f'Unsupported RFID format: {uid}')

if __name__ == '__main__':
    x = normalize_rfid('880480575F6A65F5')
    y = normalize_rfid('04F5656A5F5780')
    print(x == y)
    print(normalize_rfid('880480575F6A65F5'))
    print(normalize_rfid('04F5656A5F5780'))