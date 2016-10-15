from charity.models import Charity

def addCharity(**data):
  charity = Charity()
  charity.charity_name = data[charity_name]
  charity.charity_type = data[charity_type]
  charity.charity_register_id = data[charity_register_id]
  charity.charity_area_served = data[charity_area_served]
  charity.charity_total_income = data[charity_total_income]
  charity.charity_target = data[charity_target]
  charity.charity_logo = data[charity_logo]
  charity.charity_description = data[charity_description]
  charity.save()

def getAllCharity():
  return Charity.objects.all()

def selectCharityWithQuery(data):
  return Charity.objects.filter(**data)


