from rest_framework import serializers
from .models import *


class foodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImages
        fields = '__all__'

class carImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImages
        fields = '__all__'

class threadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threads
        fields = '__all__'

class carIssuesSerializer(serializers.ModelSerializer):
    car_comment = threadSerializer(many=True)
    class Meta:
        model = CarIssues
        fields = '__all__'

class foodIssuesSerializer(serializers.ModelSerializer):
    food_comment = threadSerializer(many=True)
    class Meta:
        model = FoodIssues
        fields = '__all__'

class drugIssuesSerializer(serializers.ModelSerializer):
    drug_comment = threadSerializer(many=True)
    class Meta:
        model = DrugIssues
        fields = '__all__'

class goodsIssuesSerializer(serializers.ModelSerializer):
    goods_comment = threadSerializer(many=True)
    class Meta:
        model = GoodsIssues
        fields = '__all__'

class carInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRecallInfo
        fields = '__all__'

class foodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecallsFood
        fields = '__all__'

class drugSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecallsDrugs
        fields = '__all__'

class carSerializer(serializers.ModelSerializer):
    recallInfo = carInfoSerializer(many=True)
    class Meta:
        model = RecallsCars
        fields = '__all__'

class goodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecallsGoods
        fields = '__all__'

class userSerializer(serializers.ModelSerializer):
    recalls_food = foodSerializer(many=True)
    recalls_cars = carSerializer(many=True)
    recalls_goods = goodsSerializer(many=True)
    recalls_drugs = drugSerializer(many=True)
    issues_food = foodIssuesSerializer(many=True)
    issues_cars = carIssuesSerializer(many=True)
    issues_drugs = drugIssuesSerializer(many=True)
    issues_goods = goodsIssuesSerializer(many=True)
    
    class Meta:
        model = Users
        # fields = '__all__'
        exclude = ('password',)


class reportProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportProduct
        fields = '__all__'


class AddressListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class AddressDetailSerializer(AddressListSerializer):

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)
        return address


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class WarrantySerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranty
        fields = '__all__'

class usersProductsFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users_products_food
        fields = '__all__' 