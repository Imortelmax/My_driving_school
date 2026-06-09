import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
from .forms import CreateUserForm, EditUserForm, LessonForm, PackageForm, StudentPackageForm, LessonRequestForm, CounterProposalForm
from .decorators import role_required
from .models import SchoolSettings, User, Lesson, Package, LessonRequest
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_student():
                return redirect('student_dashboard')
            if user.is_instructor():
                return redirect('instructor_dashboard')
            if user.is_secretary():
                return redirect('secretary_dashboard')
            if user.is_admin():
                return redirect('admin_dashboard')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    role = request.user.role
    if role == 'student':
        return redirect('student_dashboard')
    elif role == 'instructor':
        return redirect('instructor_dashboard')
    elif role == 'secretary':
        return redirect('secretary_dashboard')
    elif role == 'admin':
        return redirect('admin_dashboard')
    
    return redirect('login')

@role_required('student')
def student_dashboard(request):
    lessons = Lesson.objects.filter(student=request.user)
    next_lesson = Lesson.objects.filter(student=request.user, date__gte=timezone.now()).order_by('date').first()
    packages = Package.objects.filter(student=request.user)
    hours_used = sum(p.hours_used for p in packages)
    hours_total = sum(p.hours_total for p in packages)
    hours_remaining = sum(p.hours_remaining for p in packages)
    return render(request, 'school/student_dashboard.html', {
        'lessons': lessons,
        'hours_used': hours_used,
        'hours_total': hours_total,
        'hours_remaining': hours_remaining,
        'next_lesson': next_lesson
    })

@role_required('student')
def student_schedule(request):
    lessons = Lesson.objects.filter(student=request.user)
    return render(request, 'school/student_schedule.html', {
        'lessons': lessons
    })

@role_required('student')
def create_checkout_session(request):
    school_settings = SchoolSettings.get()
    if request.method == 'POST':
        form = StudentPackageForm(request.POST)
        if form.is_valid():
            hours = form.cleaned_data['hours_total']
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {'name': f'{hours} Driving Hours'},
                        'unit_amount': int(school_settings.price_per_hour * 100),
                    },
                    'quantity': hours,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success')),
                cancel_url=request.build_absolute_uri(reverse('student_buy_package')),
                metadata={
                    'student_id': request.user.pk,
                    'hours': hours,
                }
            )
            return redirect(session.url, code=303)
    else:
        form = StudentPackageForm()
    return render(request, 'school/buy_package.html', {
        'form': form,
        'price_per_hour': school_settings.price_per_hour,
    })

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        student = User.objects.get(pk=session['metadata']['student_id'])
        Package.objects.create(
            student=student,
            hours_total=int(session['metadata']['hours'])
        )
    return HttpResponse(status=200)

@role_required('student')
def payment_success(request):
    return render(request, 'school/payment_success.html')

@role_required('instructor')
def instructor_dashboard(request):
    students = User.objects.filter(lessons_as_student__instructor=request.user).distinct()
    lessons = Lesson.objects.filter(instructor = request.user)
    today_lessons = Lesson.objects.filter(instructor=request.user, date__date=timezone.now().date())
    total_hours = sum(l.duration for l in lessons)
    return render(request, 'school/instructor_dashboard.html', {
        'students': students,
        'lessons': lessons,
        'today_lessons': today_lessons,
        'total_hours': total_hours
    })

@role_required('instructor')
def instructor_schedule(request):
    lessons = Lesson.objects.filter(instructor=request.user)
    return render(request, 'school/instructor_schedule.html', {
        'lessons': lessons 
    })

@method_decorator(role_required('instructor'), name='dispatch')
class InstructorLessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'school/create_lesson.html'
    success_url = reverse_lazy('instructor_schedule')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('instructor')
        return form

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super().form_valid(form)

@method_decorator(role_required('instructor'), name='dispatch')
class InstructorLessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'school/edit_lesson.html'
    success_url = reverse_lazy('instructor_schedule')

    def get_queryset(self):
        lesson = Lesson.objects.filter(instructor=self.request.user)
        return lesson

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('instructor')
        return form

@method_decorator(role_required('instructor'), name='dispatch')
class InstructorLessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'school/delete_lesson.html'
    success_url = reverse_lazy('instructor_schedule')

    def get_queryset(self):
        lesson = Lesson.objects.filter(instructor=self.request.user)
        return lesson

@role_required('secretary')
def secretary_dashboard(request):
    students = User.objects.filter(role='student')
    instructors = User.objects.filter(role='instructor')
    lessons = Lesson.objects.all()
    no_hours_count = sum(
        1 for student in User.objects.filter(role='student')
        if sum(p.hours_remaining for p in Package.objects.filter(student=student)) == 0
    )
    return render(request, 'school/secretary_dashboard.html', {
        'students': students,
        'instructors': instructors,
        'lessons': lessons,
        'no_hours_count': no_hours_count
    })

@role_required('secretary')
def secretary_schedule(request):
    lessons = Lesson.objects.all()
    instructor_filter = request.GET.get('instructor')
    student_filter = request.GET.get('student')
    if instructor_filter:
        lessons = Lesson.objects.filter(instructor__pk=instructor_filter)
    if student_filter:
        lessons = Lesson.objects.filter(student__pk=student_filter)
    instructors = User.objects.filter(role='instructor')
    students = User.objects.filter(role='student')
    return render(request, 'school/secretary_schedule.html', {
        'lessons': lessons,
        'instructors': instructors,
        'students': students,
        'selected_instructor': instructor_filter,
        'selected_student': student_filter,
    })

@role_required('secretary')
def secretary_people(request):
    students = User.objects.filter(role='student')
    instructors = User.objects.filter(role='instructor')
    return render(request, 'school/secretary_people.html', {
        'students': students,
        'instructors': instructors
    })

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'school/create_user.html'

    def get_success_url(self):
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_people')
        return reverse_lazy('secretary_people')

    def get_initial(self):
        initial = super().get_initial()
        preset_role = self.request.GET.get('role', '')
        if preset_role:
            initial['role'] = preset_role
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role == 'secretary':
            form.fields['role'].choices = [
                (User.STUDENT, 'Student'),
                (User.INSTRUCTOR, 'Instructor'),
            ]
        return form

    def form_valid(self, form): 
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = 'admin_people' if self.request.user.role == 'admin' else 'secretary_people'
        return context

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'school/edit_user.html'

    def get_success_url(self):
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_people')
        return reverse_lazy('secretary_people')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role == 'secretary':
            form.fields['role'].choices = [
                (User.STUDENT, 'Student'),
                (User.INSTRUCTOR, 'Instructor'),
            ]
        return form

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'school/delete_user.html'

    def get_success_url(self):
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_people')
        return reverse_lazy('secretary_people')

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'school/create_lesson.html'
    success_url = reverse_lazy('secretary_schedule')

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'school/edit_lesson.html'
    success_url = reverse_lazy('secretary_schedule')

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'school/delete_lesson.html'
    success_url = reverse_lazy('secretary_schedule')

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class PackageCreateView(CreateView):
    model = Package
    form_class = PackageForm
    template_name = 'school/create_package.html'
    success_url = reverse_lazy('secretary_people')

    def get_initial(self):
        initial = super().get_initial()
        student_pk = self.request.GET.get('student')
        if student_pk:
            initial['student'] = student_pk
        return initial

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageForm
    template_name = 'school/edit_package.html'
    success_url = reverse_lazy('secretary_people')

@method_decorator(role_required('secretary', 'admin'), name='dispatch')
class PackageDeleteView(DeleteView):
    model = Package
    template_name = 'school/delete_package.html'
    success_url = reverse_lazy('secretary_people')

@role_required('admin')
def admin_dashboard(request):
    students = User.objects.filter(role='student')
    instructors = User.objects.filter(role='instructor')
    secretaries = User.objects.filter(role='secretary')
    lessons = Lesson.objects.all()
    no_hours_count = sum(
        1 for student in students
        if sum(p.hours_remaining for p in Package.objects.filter(student=student)) == 0
    )
    return render(request, 'school/admin_dashboard.html', {
        'students': students,
        'instructors': instructors,
        'secretaries': secretaries,
        'lessons': lessons,
        'no_hours_count': no_hours_count
    })

@role_required('admin')
def admin_schedule(request):
    lessons = Lesson.objects.all()
    instructor_filter = request.GET.get('instructor')
    student_filter = request.GET.get('student')
    if instructor_filter:
        lessons = Lesson.objects.filter(instructor__pk=instructor_filter)
    if student_filter:
        lessons = Lesson.objects.filter(student__pk=student_filter)
    instructors = User.objects.filter(role='instructor')
    students = User.objects.filter(role='student')
    return render(request, 'school/admin_schedule.html', {
        'lessons': lessons,
        'instructors': instructors,
        'students': students,
        'selected_instructor': instructor_filter,
        'selected_student': student_filter,
    })

@role_required('admin')
def admin_people(request):
    students = User.objects.filter(role='student')
    instructors = User.objects.filter(role='instructor')
    secretaries = User.objects.filter(role='secretary')
    return render(request, 'school/admin_people.html', {
        'students': students,
        'instructors': instructors,
        'secretaries': secretaries
    })

@role_required('instructor', 'secretary', 'admin')
def student_detail(request, pk):
    student = get_object_or_404(User, pk=pk)
    if request.user.is_instructor():
        if not Lesson.objects.filter(student=student, instructor=request.user).exists():
            return redirect('instructor_dashboard')
    packages = Package.objects.filter(student=student)
    lessons = Lesson.objects.filter(student=student)
    hours_total = sum(p.hours_total for p in packages)
    hours_used = sum(p.hours_used for p in packages)
    hours_remaining = sum(p.hours_remaining for p in packages)
    return render(request, 'school/student_detail.html', {
        'student': student,
        'packages': packages,
        'lessons': lessons,
        'hours_total': hours_total,
        'hours_used': hours_used,
        'hours_remaining': hours_remaining
    })

@role_required('student')
def student_lesson_requests(request):
    requests = LessonRequest.objects.filter(student=request.user).order_by('-id')
    return render(request, 'school/student_lesson_requests.html', {'requests': requests})

@role_required('student')
def student_create_lesson_request(request):
    if request.method == 'POST':
        form = LessonRequestForm(request.POST)
        if form.is_valid():
            lesson_request = form.save(commit=False)
            lesson_request.student = request.user
            lesson_request.proposed_by = LessonRequest.STUDENT
            lesson_request.save()
            return redirect('student_lesson_requests')
    else:
        form = LessonRequestForm()
    return render(request, 'school/create_lesson_request.html', {'form': form})

@role_required('student')
def student_respond_lesson_request(request, pk):
    lesson_request = get_object_or_404(LessonRequest, pk=pk, student=request.user)
    if lesson_request.proposed_by != LessonRequest.INSTRUCTOR or not lesson_request.is_pending():
        return redirect('student_lesson_requests')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            try:
                Lesson.objects.create(
                    student=lesson_request.student,
                    instructor=lesson_request.instructor,
                    date=lesson_request.date,
                    location=lesson_request.location,
                    duration=lesson_request.duration,
                )
                lesson_request.status = LessonRequest.ACCEPTED
                lesson_request.save()
            except ValidationError as e:
                form = CounterProposalForm()
                return render(request, 'school/respond_lesson_request.html', {
                    'lesson_request': lesson_request,
                    'form': form,
                    'error': e.message,
                    'responder': 'student',
                })
        elif action == 'refuse':
            lesson_request.status = LessonRequest.REFUSED
            lesson_request.save()
        elif action == 'counter':
            form = CounterProposalForm(request.POST)
            if form.is_valid():
                lesson_request.date = form.cleaned_data['date']
                lesson_request.location = form.cleaned_data['location']
                lesson_request.duration = form.cleaned_data['duration']
                lesson_request.proposed_by = LessonRequest.STUDENT
                lesson_request.save()
            else:
                return render(request, 'school/respond_lesson_request.html', {
                    'lesson_request': lesson_request,
                    'form': form,
                    'responder': 'student',
                })
        return redirect('student_lesson_requests')

    form = CounterProposalForm(initial={
        'date': lesson_request.date.strftime('%Y-%m-%dT%H:%M'),
        'location': lesson_request.location,
        'duration': lesson_request.duration,
    })
    return render(request, 'school/respond_lesson_request.html', {
        'lesson_request': lesson_request,
        'form': form,
        'responder': 'student',
    })

@role_required('instructor')
def instructor_lesson_requests(request):
    requests = LessonRequest.objects.filter(instructor=request.user).order_by('-id')
    return render(request, 'school/instructor_lesson_requests.html', {'requests': requests})

@role_required('instructor')
def instructor_respond_lesson_request(request, pk):
    lesson_request = get_object_or_404(LessonRequest, pk=pk, instructor=request.user)
    if lesson_request.proposed_by != LessonRequest.STUDENT or not lesson_request.is_pending():
        return redirect('instructor_lesson_requests')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            try:
                Lesson.objects.create(
                    student=lesson_request.student,
                    instructor=lesson_request.instructor,
                    date=lesson_request.date,
                    location=lesson_request.location,
                    duration=lesson_request.duration,
                )
                lesson_request.status = LessonRequest.ACCEPTED
                lesson_request.save()
            except ValidationError as e:
                form = CounterProposalForm()
                return render(request, 'school/respond_lesson_request.html', {
                    'lesson_request': lesson_request,
                    'form': form,
                    'error': e.message,
                    'responder': 'instructor',
                })
        elif action == 'refuse':
            lesson_request.status = LessonRequest.REFUSED
            lesson_request.save()
        elif action == 'counter':
            form = CounterProposalForm(request.POST)
            if form.is_valid():
                lesson_request.date = form.cleaned_data['date']
                lesson_request.location = form.cleaned_data['location']
                lesson_request.duration = form.cleaned_data['duration']
                lesson_request.proposed_by = LessonRequest.INSTRUCTOR
                lesson_request.save()
            else:
                return render(request, 'school/respond_lesson_request.html', {
                    'lesson_request': lesson_request,
                    'form': form,
                    'responder': 'instructor',
                })
        return redirect('instructor_lesson_requests')

    form = CounterProposalForm(initial={
        'date': lesson_request.date.strftime('%Y-%m-%dT%H:%M'),
        'location': lesson_request.location,
        'duration': lesson_request.duration,
    })
    return render(request, 'school/respond_lesson_request.html', {
        'lesson_request': lesson_request,
        'form': form,
        'responder': 'instructor',
    })