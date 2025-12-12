from foxypack import FoxyPack
from tests.foxypack_abc.test_foxyanalysis import FakeAnalysis


def test_add_new_foxypack_analysis_channel():
    foxy_stat = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxy_stat.get_analysis("https://fakesocialmedia.com/qsgqsdrr")
    assert analysis.url == 'https://fakesocialmedia.com/qsgqsdrr'
    assert analysis.social_platform == 'FakeSocialMedia'
    assert analysis.type_content == 'channel'

def test_add_new_foxypack_analysis_video():
    foxy_stat = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxy_stat.get_analysis("https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs")
    assert analysis.url == 'https://fakesocialmedia.com/qsgqsdr?content_id=video_fdasfdgfs'
    assert analysis.social_platform == 'FakeSocialMedia'
    assert analysis.type_content == 'video'

def test_invalid_link_foxypack():
    foxy_stat = FoxyPack().with_foxy_analysis(FakeAnalysis())
    analysis = foxy_stat.get_analysis("https://invalidmedia.com/qsgqsdr?content_id=video_fdasfdgfs")
    assert analysis is None