from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from lekipohodivplaninata.base.models import SiteEvaluation


class TestSiteEvaluationModel(TestCase):
    VALID_SITE_EVALUATION_DATA = {
        'assessment': 5,
        'comment': 'Test Comment',
        'rated_in': datetime.now()
    }

    def _create_and_save_evaluation(self, data):
        site_evaluation = SiteEvaluation.objects.create(**data)
        site_evaluation.full_clean()
        site_evaluation.save()
        return site_evaluation

    def test_create_site_evaluation__when_valida_data__expect_to_be_created(self):
        site_evaluation = self._create_and_save_evaluation(self.VALID_SITE_EVALUATION_DATA)
        self.assertEqual(SiteEvaluation.objects.count(), 1)
        self.assertEqual(site_evaluation.assessment, self.VALID_SITE_EVALUATION_DATA['assessment'])

    def test_create_site_evaluation__when_assessment_is_smaller_then_min_value__expect_to_raise_exception(self):
        assessment = SiteEvaluation.ASSESSMENT_MIN_VALUE - 1
        with self.assertRaises(ValidationError):
            site_evaluation_data = {**self.VALID_SITE_EVALUATION_DATA, 'assessment': assessment}
            self._create_and_save_evaluation(site_evaluation_data)

    def test_create_site_evaluation__when_assessment_is_equal_to_min_value__expect_to_be_created(self):
        assessment = SiteEvaluation.ASSESSMENT_MIN_VALUE
        site_evaluation_data = {**self.VALID_SITE_EVALUATION_DATA, 'assessment': assessment}

        site_evaluation = self._create_and_save_evaluation(site_evaluation_data)

        self.assertEqual(SiteEvaluation.objects.count(), 1)
        self.assertEqual(site_evaluation.assessment, assessment)

    def test_create_site_evaluation__when_assessment_is_bigger_then_max_value__expect_to_raise_exception(self):
        assessment = SiteEvaluation.ASSESSMENT_MAX_VALUE + 1
        with self.assertRaises(ValidationError):
            site_evaluation_data = {**self.VALID_SITE_EVALUATION_DATA, 'assessment': assessment}
            self._create_and_save_evaluation(site_evaluation_data)

    def test_create_site_evaluation__when_assessment_is_equal_to_max_value__expect_to_be_created(self):
        assessment = SiteEvaluation.ASSESSMENT_MAX_VALUE
        site_evaluation_data = {**self.VALID_SITE_EVALUATION_DATA, 'assessment': assessment}

        site_evaluation = self._create_and_save_evaluation(site_evaluation_data)

        self.assertEqual(SiteEvaluation.objects.count(), 1)
        self.assertEqual(site_evaluation.assessment, assessment)

    def test_create_site_evaluation__when_assessment_is_null__expect_to_be_created(self):
        assessment = None
        with self.assertRaises(ValidationError):
            site_evaluation_data = {**self.VALID_SITE_EVALUATION_DATA, 'assessment': assessment}
            self._create_and_save_evaluation(site_evaluation_data)

    def test_create_site_evaluation__when_comment_is_null__expect_to_be_created(self):
        comment = None
        site_evaluation_data = {**self.VALID_SITE_EVALUATION_DATA, 'comment': comment}

        site_evaluation = self._create_and_save_evaluation(site_evaluation_data)

        self.assertEqual(SiteEvaluation.objects.count(), 1)
        self.assertEqual(site_evaluation.comment, comment)
