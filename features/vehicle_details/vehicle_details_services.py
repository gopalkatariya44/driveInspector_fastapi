import os
from urllib import request
from uuid import UUID
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import pdfkit
# import pdfkit

from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates

from common.pdf_html import pdf_html
from features import templates
from features.vehicle_details.vehicle_details_model import VehicleDetailsModel

from features import templates


class VehicleDetailsServices:
    """
    Store data in database
    """

    @staticmethod
    async def get_list(user_id: UUID, page: int = 1, limit: int = 10):
        try:
            vehicle_details_list = await (VehicleDetailsModel.find(
                VehicleDetailsModel.soft_delete == False
            )
                                          # .skip(page).limit(limit)
                                          .to_list())
            return vehicle_details_list
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somthing went wrong in returning vehicle details list get_list."
            )

    @staticmethod
    async def get_one(id: ObjectId):
        try:
            vehicle_details = await VehicleDetailsModel.find_one(VehicleDetailsModel.id == id)
            return vehicle_details
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somthing went wrong in returning vehicle details get_one."
            )

    @staticmethod
    async def get_by_regno(reg_no: str):
        # try:
        print(reg_no)
        vehicle_details = await VehicleDetailsModel.find_one(VehicleDetailsModel.reg_no == reg_no)
        print(vehicle_details)
        return vehicle_details
        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Somthing went wrong in returning vehicle details get_one."
        #     )

    @staticmethod
    async def update(id: UUID, data):
        vehicle_details = await VehicleDetailsModel.find_one(VehicleDetailsModel.id == id)

        await vehicle_details.update({"$set": data})
        await vehicle_details.save()
        return vehicle_details

    @staticmethod
    async def delete(id: ObjectId):
        vehicle_details = await VehicleDetailsServices.get_one(id)
        if vehicle_details:
            # await detection_details.delete()
            await vehicle_details.update({"$set": {"soft_delete": True}})
            return {"Msg": "Project deleted successful."}
        else:
            return {"Msg": "Project not available."}

    @staticmethod
    async def generate_challan_pdf(reg_no: str):
        vehicle_details = await VehicleDetailsModel.find_one(VehicleDetailsModel.reg_no == reg_no)
        email_id = vehicle_details.email_id
        insurance_upto = vehicle_details.insurance_details['insurance_upto']
        puc_upto = vehicle_details.puc_details['puc_upto']

        date_format = '%Y-%m-%dT%H:%M:%SZ'
        today = datetime.now().date()

        insurance_bool = today < (datetime.strptime(insurance_upto, date_format)).date()
        puc_bool = today < (datetime.strptime(puc_upto, date_format)).date()

        data = {"reg_no": reg_no,
                "name": vehicle_details.owner_name,
                "address": vehicle_details.current_address_line1 + vehicle_details.current_address_line2 +
                           vehicle_details.current_address_line3,
                "vehicle_maker": vehicle_details.vehicle_manufacturer_name,
                "vehicle_model": vehicle_details.model,
                "vehicle_type": vehicle_details.vehicle_catg,
                "mobile_number": vehicle_details.mobile_no,
                "date_of_violation": today}

        subject = ""
        body = ""
        tmp = None
        if not insurance_bool and not puc_bool:
            print("not insurance_bool and puc_bool")
            subject = "Urgent Action Required: Invalid PUC and Insurance - Challan Generated"
            body = """
            I hope this message finds you well.
            
            I am writing to bring to your attention an issue regarding your vehicle.
            Our records indicate that your Proof of Pollution Under Control (PUC) and insurance documents are invalid, 
            which has resulted in the generation of a challan.
            
            It is imperative to rectify this situation promptly to avoid further penalties and ensure compliance with
            legal requirements.
            
            Kindly take immediate action to renew your PUC and insurance to avoid any inconvenience or legal
            repercussions.
            
            Should you require any assistance or clarification, please do not hesitate to contact us.
            
            Your cooperation in this matter is greatly appreciated.
            """

            puc_offence = {"offence_desc": "INVALID PUC DOCUMENT",
                           "section": "190(2)",
                           "fine_amt": "1000"}

            insurance_offence = {"offence_desc": "DRIVING UNINSURED VEHICLE",
                                 "section": "196",
                                 "fine_amt": "2000"}

            tmp = templates.TemplateResponse('pdf.html',
                                             {'request': request,
                                              'data': data,
                                              'puc_offence': puc_offence,
                                              'insurance_offence': insurance_offence})

        if (insurance_bool is True and puc_bool is False) or (insurance_bool is False and puc_bool is True):
            print("(insurance_bool is True and puc_bool is False) or (insurance_bool is False and puc_bool is True)")
            subject = "Action Required: Invalid PUC or Insurance - Challan Generated"
            body = """I hope this message finds you well.
            
            I am writing to bring to your attention an issue regarding your vehicle's documentation.
            Our records indicate that either your Proof of Pollution Under Control (PUC) or insurance document is
            invalid, which has resulted in the generation of a challan.
            
            To ensure compliance with legal requirements and avoid further penalties, it is essential to rectify
            this situation promptly. Kindly take immediate action to renew either your PUC or insurance, depending
            on the invalid document, to avoid any inconvenience or legal repercussions.
            
            Should you require any assistance or clarification, please do not hesitate to contact us.
            
            Your cooperation in this matter is greatly appreciated."""

            if insurance_bool:
                insurance_offence = {"offence_desc": "DRIVING UNINSURED VEHICLE",
                                     "section": "196",
                                     "fine_amt": "2000"}

                tmp = templates.TemplateResponse('pdf.html',
                                                 {'request': request,
                                                  'data': data,
                                                  'puc_offence': None,
                                                  'insurance_offence': insurance_offence})
            else:
                puc_offence = {"offence_desc": "INVALID PUC DOCUMENT",
                               "section": "190(2)",
                               "fine_amt": "1000"}

                tmp = templates.TemplateResponse('pdf.html',
                                                 {'request': request,
                                                  'data': data,
                                                  'puc_offence': puc_offence,
                                                  'insurance_offence': None})

        if insurance_bool and puc_bool:
            subject = "Confirmation: Valid PUC and Insurance"
            body = """I hope this message finds you well.
            
                I am pleased to inform you that our records indicate that your Proof of Pollution Under Control (PUC) 
                and insurance documents are up-to-date and valid. Your compliance in this matter is greatly appreciated, 
                and there are no issues regarding your vehicle's documentation.
                
                Thank you for ensuring that your PUC and insurance are current.
                
                By maintaining these documents, you contribute to road safety and compliance with legal requirements.
                Should you have any further questions or need assistance, please feel free to reach out to us.
                
                Your continued cooperation is valued."""

        message = MIMEMultipart()
        message["From"] = 'driveinspector81@outlook.com'
        message["To"] = email_id
        message["Subject"] = subject

        # Attach body
        message.attach(MIMEText(body, "plain"))

        os.makedirs(f"static/pdf", exist_ok=True)
        # Attach PDF
        # if ((not insurance_bool and not puc_bool) or (insurance_bool is True and puc_bool is False) or
        #         insurance_bool is False and puc_bool is True):
        # if not insurance_bool or not puc_bool:
        #     # pdf_bytes = await tmp.body()
        #     # pdfkit.from_string(pdf_html.format(reg_no=reg_no,name=vehicle_details.owner_name),
        #     #                  'static/pdf/challan.pdf',
        #     #                  options={"enable-local-file-access": ""})
        #     pdfkit.from_string(pdf_html.format(reg_no=reg_no, name=vehicle_details.owner_name),
        #                        'static/pdf/challan.pdf', options={"enable-local-file-access": ""})
        #
        #     with open("static/pdf/challan.pdf", "rb") as attachment:
        #         part = MIMEApplication(attachment.read(), _subtype="pdf")
        #
        #         part.add_header('Content-Disposition', 'attachment', filename="challan.pdf")
        #         message.attach(part)

        try:
            smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        except Exception as e:
            print(e)
            smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)

        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('driveinspector81@outlook.com', "hh^xU6u5zWDT9^i")

        smtpObj.sendmail('driveinspector81@outlook.com', email_id, message.as_string())

        smtpObj.quit()
