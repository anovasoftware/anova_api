class PersonUtilities:
    @staticmethod
    def get_full_name(first, middle, last, salutation):
        full_name = f'{last}, {first}' + ' '.join(p.strip() for p in [middle, salutation] if p)
        return full_name
