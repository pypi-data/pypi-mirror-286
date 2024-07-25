import unittest
import sys

sys.path.insert(0, "..")
sys.path.insert(0, ".")

import srtseg

sseg = srtseg.SRTSeg("example.srt")


class TestBasic(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(len(sseg.segments), 3)

    def test_m3u8(self):
        self.assertEqual(
            sseg.m3u8(),
            """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-TARGETDURATION:40
#EXT-X-DISCONTINUITY
#EXTINF:39.4,
example/0.ts
#EXT-X-DISCONTINUITY
#EXTINF:11.9,
example/1.ts
#EXT-X-DISCONTINUITY
#EXTINF:12.1,
example/2.ts
#EXT-X-ENDLIST
""",
        )

    def test_subs(self):
        self.assertEqual(sseg.srtstr().strip(), open("example.srt").read())

    def test_filename_func(self):
        self.assertEqual(sseg.media_url_func.__name__, "default_filename_func")

    def test_filename_func_m3u8(self):
        sseg2 = srtseg.SRTSeg("example.srt")
        sseg2.media_url_func = (
            lambda x: "https://mirav.cn/examples/" + str(x.subtitle.index) + ".ts"
        )
        self.assertEqual(sseg2.m3u8().splitlines()[6], "https://mirav.cn/examples/1.ts")


if __name__ == "__main__":
    unittest.main()
