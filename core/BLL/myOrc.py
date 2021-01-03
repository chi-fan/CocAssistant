import sqlite3
from utils.Logger import getLogger

LOGGING = getLogger("CocAssistant.myOrc")

class Character(object) :
    m_hash = None
    m_point = None
    m_value = None
    def __init__ (self) :
        self._connet = sqlite3.connect('E:\\cocAssistant\\core\\db\\myOrc.db')
        self._cursor = self._connet.cursor()

    def setChar(self, m_point, m_hash, m_value = None) :
        if not self.hasChar(m_hash) :
            if m_value :
                m_state = True
            else :
                m_state = False
            self._cursor.execute("insert into Font (state, value, point, hash) values (?, ?, ?, ?)", (m_state, m_value, m_point, m_hash))
            self._connet.commit()
            LOGGING.debug(f"insert state = {m_state}, value = {m_value}, point = {m_point}, hash = {m_hash} into Font")
            return True
        else :
            LOGGING.debug(f"can not insert value = {m_value}, point = {m_point}, hash = {m_hash} into Font")
            return False

    def hasChar(self, m_hash) :
            self._cursor.execute("select state from Font where hash == ?", (m_hash,))
            if self._cursor.fetchone() :
                # LOGGING.debug("has charact in Font")
                return True
            else :
                LOGGING.debug("can not find charact in Font")
                return False

    def updateChar(self, m_value, m_hash) :
        if self.hasChar(m_hash) :
            self._cursor.execute("update Font set value = ?, state = true where hash == ?", (m_value, m_hash,))
            self._connet.commit()
            LOGGING.debug(f"update value = {m_value}, hash = {m_hash} into Font" )
            return True
        else :
            LOGGING.debug(f"can not update value = {m_value}, hash = {m_hash} into Font")
            return False

if __name__ == "__main__" :
    m_charact = Character()
    print(m_charact.hasChar(88))
    m_charact.updateChar('c', 99)
    m_charact.setChar("191", 145)
    print(m_charact.setChar("191", 133, 14))
