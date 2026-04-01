class Logic():
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def andF(self, p, q):
        """'and' operator"""
        if p and q:
            return True
        if p and not q:
            return False
        if not p and q:
            return False
        if not p and not q:
            return False

    def orF(self, p, q):
        """'or' operator"""
        if p and q:
            return True
        if p and not q:
            return True
        if not p and q:
            return True
        if not p and not q:
            return False

    def ifF(self, p, q):
        """'conditional' operator"""
        if p and q:
            return True
        if p and not q:
            return False
        if not p and q:
            return True
        if not p and not q:
            return True

    def notF(self):
        """negation operator"""
        if self.p:
            return not self.p
        if self.q:
            return not self.q
        if not self.p:
            return self.p
        if not self.q:
            return self.q
