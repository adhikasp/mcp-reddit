import os
import unittest
from unittest import mock

import mcp_reddit.reddit_fetcher as reddit_fetcher


class CreateClientTests(unittest.TestCase):
    def test_authenticated_client_used_when_all_credentials_present(self) -> None:
        fake_factory = mock.Mock(return_value="client")
        env = {
            "REDDIT_CLIENT_ID": "id",
            "REDDIT_CLIENT_SECRET": "secret",
            "REDDIT_REFRESH_TOKEN": "refresh",
        }

        with mock.patch.dict(os.environ, env, clear=True):
            client = reddit_fetcher._create_client(factory=fake_factory)

        self.assertEqual(client, "client")
        fake_factory.assert_called_once_with("id", "secret", "refresh")

    def test_partial_credentials_fall_back_to_unauthenticated_client(self) -> None:
        fake_factory = mock.Mock(return_value="client")
        env = {"REDDIT_CLIENT_ID": "only-id"}

        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertLogs("mcp_reddit.reddit_fetcher", level="WARNING") as logs:
                client = reddit_fetcher._create_client(factory=fake_factory)

        self.assertEqual(client, "client")
        fake_factory.assert_called_once_with()
        self.assertIn("REDDIT_CLIENT_SECRET", logs.output[0])
        self.assertIn("REDDIT_REFRESH_TOKEN", logs.output[0])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
