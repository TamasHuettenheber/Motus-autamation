"""The writer MUST continue at episode 006 and respect the new cliffhanger."""
import unittest
from generate_episode import preexisting_season_history

class PreparedArcTests(unittest.TestCase):
    def test_five_existing_episodes_seeded(self):
        h=preexisting_season_history()
        self.assertEqual([x["episode_number"] for x in h],[1,2,3,4,5])
        self.assertEqual(max(x["episode_number"] for x in h)+1,6)
    def test_episode_six_starts_after_big_footprint(self):
        h=preexisting_season_history()
        self.assertIn("riesig",h[-1]["cliffhanger"].casefold())
        self.assertIn("Stern",h[-1]["cliffhanger"])
    def test_prepared_episodes_not_old_archived_ones(self):
        h=preexisting_season_history()
        self.assertTrue(all(x["episode_number"]>=1 for x in h))
        self.assertEqual(h[0]["title"],"Das Licht, das Joris Namen kannte")

if __name__=="__main__":unittest.main()
