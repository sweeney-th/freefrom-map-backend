import unittest
import datetime

from app import db
from models import Score
from strings import criterion_not_found, invalid_state
from tests.test_utils import (
    clear_database,
    create_state,
    create_category,
    create_subcategory,
    create_criterion,
)


class ScoreTestCase(unittest.TestCase):
    def setUp(self):
        self.state = create_state()
        self.category = create_category()
        self.subcategory = create_subcategory(self.category.id)
        self.criterion = create_criterion(self.subcategory.id)
        self.score = Score(
            criterion_id=self.criterion.id,
            state=self.state.code,
            meets_criterion=True,
        ).save()

    def tearDown(self):
        clear_database(db)

    def test_init(self):
        self.assertEqual(self.score.criterion_id, self.criterion.id)
        self.assertEqual(self.score.state, self.state.code)
        self.assertTrue(self.score.meets_criterion)
        self.assertTrue(isinstance(self.score.created_at, datetime.datetime))
        self.assertTrue(self.score.created_at < datetime.datetime.utcnow())

    def test_init_invalid_criterion(self):
        with self.assertRaises(ValueError) as e:
            Score(
                criterion_id=0,
                state=self.state.code,
                meets_criterion=True,
            )
        self.assertEqual(str(e.exception), criterion_not_found)

    def test_init_invalid_state_code(self):
        with self.assertRaises(ValueError) as e:
            Score(
                criterion_id=self.criterion.id,
                state='fake-state',
                meets_criterion=True,
            )
        self.assertEqual(str(e.exception), invalid_state)

    def test_serialize(self):
        expected_result = {
            'id': self.score.id,
            'criterion_id': self.criterion.id,
            'state': self.state.code,
            'meets_criterion': True,
        }

        actual_result = self.score.serialize()

        # Assert that the expected results are a subset of the actual results
        self.assertTrue(expected_result.items() <= actual_result.items())
