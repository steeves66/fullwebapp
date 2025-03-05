class SignalsTest(TestCase):
    def test_connection(self):
        result = signals.post_save.disconnect(
            receiver=my_handler, sender=Author
        )
        self.assertTrue(result)