from django.test import TestCase

from lekipohodivplaninata.base.models import Evaluation


class TestEvaluationModel(TestCase):
    VALID_EVALUATION_DATA = {
        'assessment': 5,
        'comment': 'Test Comment',
    }

    def _create_and_save_evaluation(self, data):
        evaluation = Evaluation.objects.create(**data)
        evaluation.full_clean()
        evaluation.save()
        return evaluation

    def test_create_evaluation__when_valida_data__expect_to_be_created(self):
        evaluation = self._create_and_save_evaluation(self.VALID_EVALUATION_DATA)
        self.assertEqual(Evaluation.objects.count(), 1)
        self.assertEqual(evaluation.assessment, self.VALID_EVALUATION_DATA['assessment'])

    def test_create_evaluation__when_assessment_is_smaller_then_min_value__expect_to_raise_exception(self):
        pass

    def test_create_evaluation__when_assessment_is_equal_to_min_value__expect_to_be_created(self):
        pass

    def test_create_evaluation__when_assessment_is_bigger_then_max_value__expect_to_raise_exception(self):
        pass

    def test_create_evaluation__when_assessment_is_equal_to_max_value__expect_to_be_created(self):
        pass

    def test_create_evaluation__when_assessment_is_null__expect_to_be_created(self):
        pass

    def test_create_evaluation__when_comment_is_null__expect_to_be_created(self):
        pass
