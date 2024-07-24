import pytest

from warc2zim.url_rewriting import apply_fuzzy_rules

from .utils import ContentForTests


@pytest.fixture(
    params=[
        ContentForTests(
            "foobargooglevideo.com/videoplayback?id=1576&key=value",
            "youtube.fuzzy.replayweb.page/videoplayback?id=1576",
        ),
        ContentForTests(
            "foobargooglevideo.com/videoplayback?some=thing&id=1576",
            "youtube.fuzzy.replayweb.page/videoplayback?id=1576",
        ),
        ContentForTests(
            "foobargooglevideo.com/videoplayback?some=thing&id=1576&key=value",
            "youtube.fuzzy.replayweb.page/videoplayback?id=1576",
        ),
        # videoplayback is not followed by `?`
        ContentForTests(
            "foobargooglevideo.com/videoplaybackandfoo?some=thing&id=1576&key=value"
        ),
        # No googlevideo.com in url
        ContentForTests(
            "foobargoogle_video.com/videoplaybackandfoo?some=thing&id=1576&key=value"
        ),
    ]
)
def google_videos_case(request):
    yield request.param


def test_fuzzyrules_google_videos(google_videos_case):
    assert (
        apply_fuzzy_rules(google_videos_case.input_str)
        == google_videos_case.expected_str
    )


@pytest.fixture(
    params=[
        ContentForTests(
            "www.youtube.com/get_video_info?video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),
        ContentForTests(
            "www.youtube.com/get_video_info?foo=bar&video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),
        ContentForTests(
            "www.youtube.com/get_video_info?video_id=123ah&foo=bar",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),
        ContentForTests(
            "youtube.com/get_video_info?video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),
        ContentForTests(
            "youtube-nocookie.com/get_video_info?video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),
        ContentForTests(
            "www.youtube-nocookie.com/get_video_info?video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),
        # no video_id parameter
        ContentForTests(
            "www.youtube-nocookie.com/get_video_info?foo=bar",
        ),
        # improper hostname
        ContentForTests(
            "www.youtubeqnocookie.com/get_video_info?video_id=123ah",
        ),
    ]
)
def google_video_info_case(request):
    yield request.param


def test_fuzzyrules_google_video_infos(google_video_info_case):
    assert (
        apply_fuzzy_rules(google_video_info_case.input_str)
        == google_video_info_case.expected_str
    )


@pytest.fixture(
    params=[
        ContentForTests(
            "i.ytimg.com/vi/-KpLmsAR23I/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8"
            "AEB-AH-CYAC0AWKAgwIABABGHIgTyg-MA8=&rs=AOn4CLDr-FmDmP3aCsD84l48ygBmkwHg-g",
            "i.ytimg.com.fuzzy.replayweb.page/vi/-KpLmsAR23I/thumbnail.jpg",
        ),
        ContentForTests(
            "i.ytimg.com/vi/-KpLmsAR23I/maxresdefault.png?sqp=-oaymwEmCIAKENAF8quKqQMa8"
            "AEB-AH-CYAC0AWKAgwIABABGHIgTyg-MA8=&rs=AOn4CLDr-FmDmP3aCsD84l48ygBmkwHg-g",
            "i.ytimg.com.fuzzy.replayweb.page/vi/-KpLmsAR23I/thumbnail.png",
        ),
        ContentForTests(
            "i.ytimg.com/vi/-KpLmsAR23I/maxresdefault.jpg",
            "i.ytimg.com.fuzzy.replayweb.page/vi/-KpLmsAR23I/thumbnail.jpg",
        ),
        ContentForTests(
            "i.ytimg.com/vi/-KpLmsAR23I/max-res.default.jpg",
            "i.ytimg.com.fuzzy.replayweb.page/vi/-KpLmsAR23I/thumbnail.jpg",
        ),
    ]
)
def youtube_thumbnails_case(request):
    yield request.param


def test_fuzzyrules_youtube_thumbnails(youtube_thumbnails_case):
    assert (
        apply_fuzzy_rules(youtube_thumbnails_case.input_str)
        == youtube_thumbnails_case.expected_str
    )


@pytest.fixture(
    params=[
        ContentForTests(
            "www.example.com/page?1234",
            "www.example.com/page",
        ),
        ContentForTests(
            "www.example.com/page?foo=1234",
        ),
        ContentForTests(
            "www.example.com/page1234",
        ),
        ContentForTests(
            "www.example.com/page?foo=bar&1234",
        ),
        ContentForTests(
            "www.example.com/page?1234=bar",
        ),
        ContentForTests(
            "www.example.com/page?1234&foo=bar",
        ),
    ]
)
def trim_digits_only_query_case(request):
    yield request.param


def test_fuzzyrules_trim_digits_only_query(trim_digits_only_query_case):
    assert (
        apply_fuzzy_rules(trim_digits_only_query_case.input_str)
        == trim_digits_only_query_case.expected_str
    )


@pytest.fixture(
    params=[
        ContentForTests(
            "www.youtube-nocookie.com/youtubei/page/?videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),
        ContentForTests(
            "youtube-nocookie.com/youtubei/page/?videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),
        ContentForTests(
            "youtube.com/youtubei/page/?videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),
        ContentForTests(
            "www.youtube.com/youtubei/page/?videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),
        ContentForTests(
            "youtube.com/youtubei/page/videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),
        ContentForTests(
            "youtube.com/youtubei/page/videoIdqqq=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoIdqqq=123ah",
        ),
        ContentForTests(
            "youtube.com/youtubei/page/videoId=123ah&foo=bar",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),
        ContentForTests(
            "youtube.com/youtubei/page/?foo=bar&videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),
        ContentForTests(
            "youtube.com/youtubei/page/foo=bar&videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/foo=bar&?videoId=123ah",
        ),
        ContentForTests(
            "youtube.com/youtubei/?videoId=123ah",
        ),
    ]
)
def youtubei_case(request):
    yield request.param


def test_fuzzyrules_youtubei(youtubei_case):
    assert apply_fuzzy_rules(youtubei_case.input_str) == youtubei_case.expected_str


@pytest.fixture(
    params=[
        ContentForTests(
            "www.youtube-nocookie.com/embed/foo",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),
        ContentForTests(
            "www.youtube-nocookie.com/embed/bar",
            "youtube.fuzzy.replayweb.page/embed/bar",
        ),
        ContentForTests(
            "www.youtube-nocookie.com/embed/foo/bar",
            "youtube.fuzzy.replayweb.page/embed/foo/bar",
        ),
        ContentForTests(
            "www.youtube.com/embed/foo",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),
        ContentForTests(
            "youtube.com/embed/foo",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),
        ContentForTests(
            "youtube-nocookie.com/embed/foo",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),
        ContentForTests(
            "youtube.com/embed/foo?bar=alice",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),
    ]
)
def youtube_embed_case(request):
    yield request.param


def test_fuzzyrules_youtube_embed(youtube_embed_case):
    assert (
        apply_fuzzy_rules(youtube_embed_case.input_str)
        == youtube_embed_case.expected_str
    )


@pytest.fixture(
    params=[
        ContentForTests(
            "gcs-vimeo.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),
        ContentForTests(
            "vod.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),
        ContentForTests(
            "vod-progressive.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),
        ContentForTests(
            "vod-adaptive.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),
        ContentForTests(
            "vod.akamaized.net/123.mp4?foo=bar&range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),
        ContentForTests(
            "vod.akamaized.net/123.mp4?foo=bar&range=123-456&bar=foo",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),
        ContentForTests(
            "vod.akamaized.net/123.mp4?range=123-456&bar=foo",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),
        ContentForTests(
            "foovod.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),
        ContentForTests(
            "vod.akamaized.net/1/23.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/23.mp4?range=123-456",
        ),
        ContentForTests(
            "vod.akamaized.net/a/23.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/23.mp4?range=123-456",
        ),
        ContentForTests(
            "vod.akamaized.net/foo/bar/23.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/23.mp4?range=123-456",
        ),
        ContentForTests(
            "foo.akamaized.net/123.mp4?range=123-456",
        ),
        ContentForTests(
            "vod.akamaized.net/23.mp4",
            "vimeo-cdn.fuzzy.replayweb.page/23.mp4",
        ),
        ContentForTests(
            "vod.akamaized.net/23/12332.mp4",
            "vimeo-cdn.fuzzy.replayweb.page/23/12332.mp4",
        ),
        ContentForTests(
            "https://vod-progressive.akamaized.net/exp=1635528595"
            "~acl=%2Fvimeo-prod-skyfire-std-us"
            "%2F01%2F4423%2F13%2F347119375%2F1398505169.mp4"
            "~hmac=27c31f1990aab5e5429f7f7db5b2dcbcf8d2f5c92184d53102da36920d33d53e"
            "/vimeo-prod-skyfire-std-us/01/4423/13/347119375/1398505169.mp4",
            "vimeo-cdn.fuzzy.replayweb.page/01/4423/13/347119375/1398505169.mp4",
        ),
    ]
)
def vimeo_cdn_case(request):
    yield request.param


def test_fuzzyrules_vimeo_cdn(vimeo_cdn_case):
    assert apply_fuzzy_rules(vimeo_cdn_case.input_str) == vimeo_cdn_case.expected_str


@pytest.fixture(
    params=[
        ContentForTests(
            "player.vimeo.com/video/123?foo=bar",
            "vimeo.fuzzy.replayweb.page/video/123",
        ),
        ContentForTests(
            "foo.player.vimeo.com/video/123?foo=bar",
            "vimeo.fuzzy.replayweb.page/video/123",
        ),
        ContentForTests(
            "player.vimeo.com/video/1/23?foo=bar",
        ),
        ContentForTests(
            "player.vimeo.com/video/123a?foo=bar",
        ),
        ContentForTests(
            "player.vimeo.com/video/?foo=bar",
        ),
    ]
)
def vimeo_host_case(request):
    yield request.param


def test_fuzzyrules_vimeo_host(vimeo_host_case):
    assert apply_fuzzy_rules(vimeo_host_case.input_str) == vimeo_host_case.expected_str
