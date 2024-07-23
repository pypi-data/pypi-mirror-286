from .models import Company
import logging


def create_company(name: str, **kwargs):
   try:
      if 'name' in kwargs: kwargs.pop('name', None)
      c = Company(name=name, **kwargs)
      c.save()
      return c
   except Exception as e:
      logging.error(f"Failed to create company: {str(e)}")

def read_company(pk: str):
   try:
      company = Company.find(Company.pk==pk).first()
      logging.info(f"Company {pk} found")
      return company
   except Exception:
     logging.error(f"Company {pk} not found.")

def read_company_by_name(name: str):
   try:
      company = Company.find(Company.name==name).first()
      logging.info(f"Company {name} found")
      return company
   except Exception:
     logging.error(f"Company {name} not found.")

def update_company(pk: str, **kwargs):
   try:
      c = read_company(pk)
      logging.info(f"Found company: {c.name}")
      if kwargs: 
         c.__dict__.update(kwargs)
         c.save()
         return c
   except Exception as e:
      logging.info(f"Error updating company {pk}: {str(e)}")


def delete_company(pk: str):
   pass