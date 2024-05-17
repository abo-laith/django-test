from functools import wraps
from django.db import OperationalError, ProgrammingError
from django.http import HttpResponseServerError


def handle_database_error(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            # تنفيذ العرض المطلوب
            return view_func(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            # في حالة حدوث خطأ في قاعدة البيانات، يتم تنفيذ هذا الكود
            return HttpResponseServerError("خطأ: لا يمكن الوصول إلى قاعدة البيانات حاليًا. يرجى المحاولة مرة أخرى لاحقًا.")

    return _wrapped_view