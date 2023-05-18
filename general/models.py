from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
import uuid

# Create your models here.

class CarImages(models.Model):
    make = models.CharField(blank=False, max_length=255, null=True)
    model = models.CharField(blank=False, max_length=255, null=True)
    year = models.CharField(blank=False, max_length=255, null=True)
    image = models.CharField(blank=False, max_length=255, null=True)

class FoodImages(models.Model):
    name = models.CharField(blank=False, max_length=200, null=True)
    image = models.CharField(blank=False, max_length=255, null=True)

class CarRecallInfo(models.Model):
    make = models.CharField(blank=False, max_length=255, null=True)
    model = models.CharField(blank=False, max_length=255, null=True)
    year = models.CharField(blank=False, max_length=255, null=True)
    manufacturer = models.CharField(blank=False, max_length=255, null=True)
    NHTSAcampaignnumber = models.CharField(blank=False, max_length=255, null=True)
    reportReceivedDate = models.CharField(blank=False, max_length=255, null=True)
    Summary = models.CharField(blank=False, max_length=1000, null=True)
    Conequence  = models.CharField(blank=False, max_length=1000, null=True)
    Remedy = models.CharField(blank=False, max_length=100, null=True)
    Component = models.CharField(blank=False, max_length=255, null=True)
    Notes = models.CharField(blank=False, max_length=255, null=True) 

class RecallsFood(models.Model):
    Product_Name = models.CharField(blank=False, max_length=255, null=True)
    UPCs = models.CharField(max_length=255, null=True)
    Product_Type = models.CharField(blank=False, max_length=255, null=True)
    Recall_Init_Date = models.CharField(blank=False, max_length=255, null=True)
    Recall_City = models.CharField(blank=False, max_length=255, null=True)
    Recall_State = models.CharField(blank=False, max_length=255, null=True)
    Recall_Zip = models.CharField(blank=False, max_length=255, null=True)
    Recall_Distribution = models.CharField(blank=False, max_length=500, null=True)
    Recall_Reason = models.CharField(blank=False, max_length=500, null=True)
    Recall_Number = models.CharField(blank=False, max_length=255, null=True, unique=True)
    Product_Description = models.CharField(blank=False, max_length=500, null=True)
    date = models.DateField(auto_now=True, null=True)

class RecallsDrugs(models.Model):
    DrugName = models.CharField(blank=False, max_length=255, null=True)
    NDCs = models.CharField(max_length=255, null=True)
    DrugType = models.CharField(blank=False, max_length=255, null=True)
    RecallInitiationDate = models.CharField(blank=False, max_length=255, null=True)
    RecallCity = models.CharField(blank=False, max_length=255, null=True)
    RecallState = models.CharField(blank=False, max_length=255, null=True)
    RecallZip = models.CharField(blank=False, max_length=255, null=True)
    RecallDistribution  = models.CharField(blank=False, max_length=255, null=True)
    RecallReason = models.CharField(blank=False, max_length=255, null=True)
    RecallNumber = models.CharField(blank=False, max_length=255, null=True, unique=True)
    ProductDescription = models.CharField(blank=False, max_length=255, null=True)
    date = models.DateField(auto_now=True, null=True)

class RecallsCars(models.Model):
    make = models.CharField(blank=False, max_length=255, null=True)
    model = models.CharField(blank=False, max_length=255, null=True)
    year = models.CharField(blank=False, max_length=255, null=True)
    date = models.DateField(auto_now=True, null=True)
    # do many to many
    recallInfo = models.ManyToManyField(CarRecallInfo)

class RecallsGoods(models.Model):
    name = models.CharField(blank=False, max_length=255, null=True)
    title = models.CharField(blank=False, max_length=255, null=True)
    recallDate = models.CharField(blank=False, max_length=255, null=True)
    recallNumber = models.CharField(blank=False, max_length=255, null=True, unique=True)
    description = models.CharField(blank=False, max_length=500, null=True)
    url = models.CharField(blank=False, max_length=255, null=True)
    consumerContact = models.CharField(blank=False, max_length=255, null=True)
    image = models.CharField(blank=False, max_length=255, null=True)
    inguries = models.CharField(blank=False, max_length=255, null=True)
    manufacturers = models.CharField(blank=False, max_length=255, null=True)
    retailers = models.CharField(blank=False, max_length=255, null=True)
    manufacturerCountries = models.CharField(blank=False, max_length=255, null=True)
    hazards = models.CharField(blank=False, max_length=500, null=True)
    remedies = models.CharField(blank=False, max_length=500, null=True)
    distributors = models.CharField(blank=False, max_length=255, null=True)
    date = models.DateField(auto_now=True, null=True)

# class UserVotes(models.Model):
#     userID = models.CharField(blank=False, max_length=50, null=True)

class Threads(models.Model):
    comment = models.CharField(blank=False, max_length=500, null=True)
    
class FoodIssues(models.Model):
    name = models.CharField(blank=False, max_length=255, null=True)
    title = models.CharField(blank=False, max_length=255, null=True)
    UPC = models.CharField(blank=False, max_length=255, null=True)
    description = models.CharField(blank=False, max_length=500, null=True)
    date = models.DateField(auto_now=True, null=True)
    votes = models.IntegerField(default=0)
    # userIDs = models.ManyToManyField(UserVotes)
    food_comment = models.ManyToManyField(Threads)

class DrugIssues(models.Model):
    name = models.CharField(blank=False, max_length=255, null=True)
    title = models.CharField(blank=False, max_length=255, null=True)
    NDC = models.CharField(blank=False, max_length=255, null=True)
    description = models.CharField(blank=False, max_length=500, null=True)
    date = models.DateField(auto_now=True, null=True)
    votes = models.IntegerField(default=0)
    #userIDs = models.ManyToManyField(UserVotes)
    drug_comment = models.ManyToManyField(Threads)

class GoodsIssues(models.Model):
    name = models.CharField(blank=False, max_length=255, null=True)
    title = models.CharField(blank=False, max_length=255, null=True)
    UPC = models.CharField(blank=False, max_length=255, null=True)
    description = models.CharField(blank=False, max_length=500, null=True)
    date = models.DateField(auto_now=True, null=True)
    votes = models.IntegerField(default=0)
    #userIDs = models.ManyToManyField(UserVotes)
    goods_comment = models.ManyToManyField(Threads)

class CarIssues(models.Model):
    make = models.CharField(blank=False, max_length=255, null=True)
    model = models.CharField(blank=False, max_length=255, null=True)
    year = models.CharField(blank=False, max_length=255, null=True)
    title = models.CharField(blank=False, max_length=255, null=True)
    description = models.CharField(blank=False, max_length=500, null=True)
    date = models.DateField(auto_now=True, null=True)
    votes = models.IntegerField(default=0)
    #userIDs = models.ManyToManyField(UserVotes)
    car_comment = models.ManyToManyField(Threads)

#----new code

ReportProduct_Choices = (
    ("Goods", "Goods"),
    ("Car", "Car"),
    ("Drug", "Drug"),
    ("Food", "Food"),

)
PreferContactMethod_Choices = (
    ("Email", "Email"),
    ("PhoneNumber", "PhoneNumber" ),
)

class ReportProduct(models.Model):
  selectProductCategory = models.CharField(
            max_length=30,
            choices=ReportProduct_Choices,
            default='Goods',
            null=True
      )

  identifyProduct = models.CharField(blank=False, max_length=255, null=False)#productName, require
  upc = models.CharField(blank=False, max_length=255, null=False) #Universal Product Code, require
  firstname = models.CharField(blank=False, max_length=255, null=True)
  lastname = models.CharField(blank=False, max_length=255, null=True)#not compulsory
  #Address = address = models.TextField(max_length=255)
  useremail = models.CharField(blank=False, max_length=255, null=False) #
  userZipCode = models.CharField(max_length=255, null=True)
  userPhoneNumber = models.CharField(max_length=255, null=False)
  preferredcontactmethod = models.CharField(
      max_length=25,
      choices=PreferContactMethod_Choices,
      default='PhoneNumber',
      null = True
  ) #
 # productBuyDate = models.DateField(null=True)
  locationOfPurchase = models.CharField(max_length=255, null=True)
  medicalCare = models.BooleanField(default=False, null=True)
  doctorName = models.CharField(blank=True, max_length=255, default='null')
  describeProblem = models.TextField(blank=True,null=True)  # user can add description about issue or not -- to make compulsion make it false
  agreeToStatement = models.BooleanField(default=False, null=False)
  #agreeToStatement1 = models.BooleanField(required = True)


class Users(AbstractBaseUser):
    username = models.CharField(blank=False, max_length=255, null=False, unique=True)
    name = models.CharField(blank=False, max_length=255, null=False)
    email = models.CharField(blank=False, max_length=255, null=False)
    agreeToTerms = models.BooleanField(default=False, null=False) # terms and conditions --
    recalls_food = models.ManyToManyField(RecallsFood) # users recalls
    recalls_drugs = models.ManyToManyField(RecallsDrugs)
    recalls_goods = models.ManyToManyField(RecallsGoods)
    recalls_cars = models.ManyToManyField(RecallsCars)
    issues_food = models.ManyToManyField(FoodIssues, related_name = "food_issue")
    votes_food = models.ManyToManyField(FoodIssues, related_name = "food_votes")
    votes_goods = models.ManyToManyField(GoodsIssues, related_name = "goods_votes")
    issues_drugs = models.ManyToManyField(DrugIssues, related_name = "drug_issue")
    votes_drug = models.ManyToManyField(DrugIssues, related_name = "drug_votes")
    issues_goods = models.ManyToManyField(GoodsIssues, related_name = "goods_issue")
    issues_cars = models.ManyToManyField(CarIssues, related_name = "car_issue")
    votes_car = models.ManyToManyField(CarIssues, related_name = "car_votes")
    #product_report = models.ManyToManyField(ReportProduct, related_name="report_product")
    USERNAME_FIELD = 'email'

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    # country = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Manufacturer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    hasserialnumber = models.BooleanField(default=False);


STATUS_CHOICES = (
    ('pending', 'pending'),
    ('successful', 'successful'),
    ('error', 'error')
)


class Warranty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serialnumber = models.CharField(max_length=255)
    unspsc = models.CharField(max_length=255)
    mfrid = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    regdate = models.DateTimeField(default=timezone.now)
    userAddress = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class Users_products_food(models.Model):
    users = models.ForeignKey(Users, default=None, on_delete=models.CASCADE)
    sifter_id = models.CharField(blank = False, max_length = 20)
    fda_id = models.CharField(blank = True, max_length=20)
    productName = models.CharField(max_length=100, null=True)




