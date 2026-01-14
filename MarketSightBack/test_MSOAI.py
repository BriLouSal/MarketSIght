from .MSOAI  import StockSummary
import unittest






class Summary_text(unittest.TestCase):
    

    def SummarizedStocks(self):
        result = StockSummary('Summarize AAPL NEWS')
        self.assertIsInstance(result, str)
        if self.assertIsInstance == None:
            return False
        else:
            return True
