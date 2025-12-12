from tests.foxypack_abc.test_foxyanalysis import FakeAnalysis

data = FakeAnalysis().get_analysis("https://fakesocialmedia.com/qsgqsdrr")
print(data)
data = FakeAnalysis().get_analysis("https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfsfdasfdgfs")
print(data)