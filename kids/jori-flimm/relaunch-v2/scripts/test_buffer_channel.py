"""Buffer connection check never accepts MOTUS or an unknown TikTok handle."""
import unittest
from check_buffer_channel import canonical_handle, validate_channels

class BufferSafetyTests(unittest.TestCase):
    def test_valid_separate_tiktok(self):
        self.assertTrue(validate_channels([{
           "id":"channel_id","name":"jori.flimm","service":"tiktok","isQueuePaused":False
        }],"jori.flimm"))
    def test_motus_is_never_target(self):
        with self.assertRaises(ValueError):
            validate_channels([{"id":"one","name":"motus614","service":"tiktok"}],"motus614")
    def test_motus_alone_does_not_count(self):
        with self.assertRaisesRegex(RuntimeError,"NOT_VERIFIED"):
            validate_channels([{"id":"one","name":"motus614","service":"tiktok"}],"jori.flimm")
    def test_paused_channel_blocks(self):
        with self.assertRaisesRegex(RuntimeError,"PAUSED"):
            validate_channels([{"id":"two","name":"jori.flimm","service":"tiktok","isQueuePaused":True}],"jori.flimm")
    def test_normalization(self):
        self.assertEqual(canonical_handle(" @Jori.Flimm "),"jori.flimm")

if __name__=="__main__":unittest.main()
