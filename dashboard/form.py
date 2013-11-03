from django import forms
from django.utils import timezone
import datetime
from dashboard.models import Customer, Contact, FuelTankType, Device
from dashboard.helper import get_inferior_roles

class CustomerLoginForm(forms.Form):
    login_name = forms.CharField(max_length=32) 
    password = forms.CharField(widget=forms.PasswordInput, max_length=128 )

    def clean(self):
        if not self._errors:
            un = self.cleaned_data.get('login_name')
            pswd = self.cleaned_data.get('password')

            # Database authentication logic
            import hashlib
            secret = hashlib.md5(pswd.encode('utf-8')).hexdigest()
            
            authenticated = False
            try:
                customer = Customer.objects.get(login_name=un)
                if customer.dirty:
                    raise forms.ValidationError("This account is shutdown.")
                if timezone.now() > customer.validity_till:
                    raise forms.ValidationError("This account is suspended.")
                if customer.passwd == secret:
                    authenticated = True
            except Customer.DoesNotExist, err:
                raise forms.ValidationError("No such account exsist.")

            if not authenticated:
                raise forms.ValidationError("Invalid credentials.")
            else:
                return self.cleaned_data
        else:
            return self.cleaned_data

class CustomerRegistrationForm(forms.Form):
    login_name = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput, max_length=128)
    name = forms.CharField(max_length=32)
    display_pic = forms.ImageField(required=False)
    address = forms.CharField(max_length=124, required=False)
    city = forms.CharField(max_length=32, required=False)
    mobile_no = forms.CharField(max_length=13, required=False)
    email_addr = forms.EmailField()
    alert_type = forms.ChoiceField( choices=( ('AUTO','Auto'),
                            ('EMAIL','EMAIL'),
                            ('SMS','SMS'),
                            ('BOTH','Both')
                        )
                )
    role = forms.ChoiceField( choices=( ('','Error') ) )
    parent = forms.ChoiceField( choices=( ('','Error') ) )
    validity_till = forms.DateField()

    def __init__(self,request,*args,**kwargs):
        super(CustomerRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['role'] = forms.ChoiceField( choices=get_inferior_roles(request.session['role']) )
        customer = Customer.objects.get(login_name=request.session['ln'])
        """
        Read at: https://tabo.pe/projects/django-treebeard/docs/tip/intro.html#basic-usage
        Returns:
            [(<Customer: root>, {'close': [0], 'level': 0L, 'open': True})]
        """
        childs = Customer.get_annotated_list(parent=customer)
        childs_tuple_list = []
        for child in childs:
           childs_tuple_list.append((child[0].login_name, ('-' * child[1]['level']) + child[0].name))
        child_tuple_tuple = tuple(childs_tuple_list)
        self.fields['parent'] = forms.ChoiceField( choices=child_tuple_tuple )

    def clean(self):
        if not self._errors:
            un = self.cleaned_data.get('login_name')
            try:
                customer = Customer.objects.get(login_name=un)
                raise forms.ValidationError("This customer is already registered.")
            except Customer.DoesNotExist, err:
                pass
            return self.cleaned_data
        else:
            return self.cleaned_data

class FuelTankTypeRegistrationForm(forms.Form):
    name = forms.CharField(max_length=32)
    level_0 = forms.IntegerField(max_value=100, min_value=0) 
    level_10 = forms.IntegerField(max_value=100, min_value=0) 
    level_20 = forms.IntegerField(max_value=100, min_value=0) 
    level_30 = forms.IntegerField(max_value=100, min_value=0) 
    level_40 = forms.IntegerField(max_value=100, min_value=0) 
    level_50 = forms.IntegerField(max_value=100, min_value=0) 
    level_60 = forms.IntegerField(max_value=100, min_value=0) 
    level_70 = forms.IntegerField(max_value=100, min_value=0) 
    level_80 = forms.IntegerField(max_value=100, min_value=0) 
    level_90 = forms.IntegerField(max_value=100, min_value=0) 
    level_100 = forms.IntegerField(max_value=100, min_value=0)

    def clean(self):
        if not self._errors:
            n = self.cleaned_data.get('name')
            try:
                FuelTankType.objects.get(name=n)
                raise forms.ValidationError("This Fuel tank type is already registered.")
            except FuelTankType.DoesNotExist, err:
                pass
            return self.cleaned_data
        else:
            return self.cleaned_data

class ContactRegistrationForm(forms.Form):
    owner = forms.ChoiceField( choices=( ('','Error') ) )
    contact_value = forms.CharField(max_length=128)
    contact_name = forms.CharField(max_length=64)
    contact_type = forms.ChoiceField( 
                        choices=(
                            ('email','Email'),
                            ('mobileno','Mobile No')
                        )
                    )


class DeviceRegistrationForm(forms.Form):
    # Device Details (REQUIRED)
    imei = forms.CharField(max_length=16)
    name = forms.CharField(max_length=32)
    protocol = forms.ChoiceField(
                     choices=(  ('TK103','TK103'),
                                ('CT04', 'CT04'),
                                ('PT300','PT300'),
                     )
                )
    icon = forms.ChoiceField(
                    choices=(
                        ('car','Car'),
                        ('bike','Bike'),
                        ('truck','Truck'),
                        ('tracker', 'Tracker'),
                    )
            )
    imsi = forms.CharField(max_length=15)
    stock_st = forms.ChoiceField(
                         choices=( ('instock','In Stock'),
                                   ('sold','Sold')
                         )
                )           
    tank_sz = forms.IntegerField(max_value=1000, min_value=0)
    fuel_tank = forms.ChoiceField( choices=( ('','Error') ) ) #Populated at runtime
    max_speed = forms.IntegerField(max_value=200, min_value=0)
    max_temp = forms.IntegerField(max_value=200, min_value=0)
    lowest_fuel = forms.IntegerField(max_value=500, min_value=0)
    subscription_amt = forms.IntegerField(max_value=1000, min_value=0)
    owner = forms.ChoiceField( choices=( ('','Error') ) ) #Populated at runtime
    # Insurance Details (OPTIONAL)
    rc_number = forms.CharField(max_length=32, required=False)
    rc_date = forms.DateField(required=False)
    insurance_number = forms.CharField(max_length=32, required=False)
    insurance_company = forms.CharField(max_length=32, required=False)
    insurance_date = forms.DateField(required=False)
    insurance_due_date = forms.DateField(required=False)
    insurance_premium = forms.IntegerField(max_value=100000, min_value=0, required=False) 
    servicing_due_date = forms.DateField(required=False)
    servicing_due_km = forms.IntegerField(max_value=1000000, min_value=0, required=False)
    odometer_reading = forms.IntegerField(max_value=1000000, min_value=0, required=False)
    # Driver Details (OPTIONAL)
    driver_dp = forms.ImageField(required=False)
    driver_name = forms.CharField(max_length=32, required=False)
    driver_addr = forms.CharField(max_length=256, required=False)
    driver_contact_no = forms.CharField(max_length=32, required=False)
    license_no = forms.CharField(max_length=32, required=False)
    license_exp_date = forms.DateField(required=False)
    # Contract Details (OPTIONAL)
    contract_company = forms.CharField(max_length=32, required=False)
    contract_amt = forms.IntegerField(max_value=500000, min_value=0, required=False)
    contract_renewal_dt = forms.DateField(required=False)
    contract_date = forms.DateField(required=False)
    

    def __init__(self,request,*args,**kwargs):
        super(DeviceRegistrationForm,self).__init__(*args,**kwargs)
        customer = Customer.objects.get(login_name=request.session['ln'])
        #Populating the Owners for the device
        childs = Customer.get_annotated_list(parent=customer)
        childs_tuple_list = []
        for child in childs:
           childs_tuple_list.append((child[0].login_name, ('-' * child[1]['level']) + child[0].name))
        self.fields['owner'] = forms.ChoiceField( choices=tuple(childs_tuple_list) )
        #Populating the Fuel Tank Type 
        ftt_tuple_list = []
        for ftt in FuelTankType.objects.all():
            ftt_tuple_list.append((ftt.id, ftt.name))
        self.fields['fuel_tank'] = forms.ChoiceField( choices=tuple(ftt_tuple_list) )

    def clean(self):
        if not self._errors:
            n = self.cleaned_data.get('imei')
            try:
                Device.objects.get(imei=n)
                raise forms.ValidationError("This device is already registered.")
            except Device.DoesNotExist, err:
                pass
            return self.cleaned_data
        else:
            return self.cleaned_data 



class CustomerUpdationForm(forms.Form):
    login_name = forms.CharField(max_length=32, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    password = forms.CharField(max_length=128)
    name = forms.CharField(max_length=32)
    display_pic = forms.ImageField(required=False)
    address = forms.CharField(max_length=124, required=False)
    city = forms.CharField(max_length=32, required=False)
    mobile_no = forms.CharField(max_length=13, required=False)
    email_addr = forms.EmailField()
    alert_type = forms.ChoiceField( choices=( ('AUTO','Auto'),
                            ('EMAIL','EMAIL'),
                            ('SMS','SMS'),
                            ('BOTH','Both')
                        )
                )
    role = forms.ChoiceField( choices=( ('','Error') ) )
    validity_till = forms.DateField()

    def __init__(self,request,*args,**kwargs):
        super(CustomerUpdationForm,self).__init__(*args,**kwargs)
        customer = Customer.objects.get(login_name=request.POST['ln'])
        self.fields['login_name'] = forms.CharField(max_length=32, widget = forms.TextInput(attrs={'readonly':'readonly'}),
                initial=customer.login_name)
        self.fields['password'] = forms.CharField(max_length=128, initial="")
        self.fields['name'] = forms.CharField(max_length=32, initial=customer.name)
        self.fields['address'] = forms.CharField(max_length=124, required=False, initial=customer.address)
        self.fields['city'] = forms.CharField(max_length=32, required=False, initial=customer.city)
        self.fields['mobile_no'] = forms.CharField(max_length=13, required=False, initial=customer.mobile_no)
        self.fields['email_addr'] = forms.EmailField(initial=customer.email_addr)
        self.fields['alert_type'] = forms.ChoiceField( choices=( ('AUTO','Auto'),
                            ('EMAIL','EMAIL'),
                            ('SMS','SMS'),
                            ('BOTH','Both')
                        ),
                        initial=customer.alert_type
                )
        self.fields['role'] = forms.ChoiceField( choices=get_inferior_roles(request.session['role']), initial=customer.role)
        self.fields['validity_till'] = forms.DateField(initial=customer.validity_till)

    def clean(self):
        if not self._errors:
            un = self.cleaned_data.get('login_name')
            try:
                customer = Customer.objects.get(login_name=un)
            except Customer.DoesNotExist, err:
                raise forms.ValidationError("No such customer.")
            return self.cleaned_data
        else:
            return self.cleaned_data

