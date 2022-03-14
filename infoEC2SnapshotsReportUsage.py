#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import boto3
import datetime
import xlsxwriter
from botocore.exceptions import ClientError

# Inicial configuration EC2
ec2 = boto3.client('ec2')

# Time 0 days ago. I mean NOW.
today = datetime.datetime.now()

# Excel Name.
excelFileName = ("Status-EC2-" + "ENVIRONMENT" +  "-" + today.strftime("%d""-""%b") + ".xlsx")

"""
  Function: infoEC2SnapshotsReportUsage()
  Input:
    AWS_PROFILE=sso-nvoperations-pu python3 infoEC2SnapshotsReportUsage.py
  Output:
    Excel in S3 with all report.
  Descr: Obtain a Excel file that contains info about Snapshots, Volumes, AMIS... to be deleted.
"""


def create_excel(excelFileName):
  # Name of file XLSX Excel that contains all info.
  print("Excel File going to be created --> "+ excelFileName)

  # Create workbook.
  workbook = xlsxwriter.Workbook(f'{excelFileName}')

  # Add MAIN worksheet to the workbook.
  main_worksheet = workbook.add_worksheet('INFORMATION')

  # Set auto filter on for the cells
  main_worksheet.autofilter('C3:M4')

  # Hide unused rows.
  main_worksheet.set_default_row(hide_unused_rows=True)

  # Define wihite backgroup format.
  whiteBackGroundFromat = workbook.add_format(
      {
          'bg_color': "#FFFFFF",
          'align': 'center',
          'valign': 'center',
          'font_name': 'calibri',
          'font_size': 11,
          'text_wrap': True,
          'locked': True,
          'border': 0
      }
  )

  # Merge Format for KP worksheet.
  mergedFormat = workbook.add_format(
      {
          'bg_color': "#000000",
          'font_color': "#FFFFFF",
          'align': 'center',
          'valign': 'center',
          'font_name': 'Segoe UI',
          'font_size': 15,
          'bold': 'True',
          'locked': 'True',
          'border': 0
      }
  )
  # Cells under Merged form.
  subMergedFormat = workbook.add_format(
      {
          'bg_color': "03C0FF",
          'font_color': "#FFFFFF",
          'align': 'vcenter',
          'valign': 'center',
          'font_name': 'Calibri',
          'font_size': 13,
          'bold': 'True',
          'locked': 'True',
          'border': 5,
          'top': 5,
          'bottom': 5,
          'left': 5,
          'right': 5,	
          'border_color': "#FFFFFF"
      }
  )

  grayFormatDark = workbook.add_format(
      {
          'bg_color': "#CDD1DE",
          'font_color': "#000000",
          'align': 'center',
          'valign': 'center',
          'text_wrap': True,
          'font_name': 'Calibri',
          'font_size': 10,
          'locked': 'True',
          'border': 4,
          'top': 4,
          'bottom': 4,
          'left': 4,
          'right': 4,	
          'border_color': "#FFFFFF"
      }
  )

  grayFormatDarkNum = workbook.add_format(
      {
          'bg_color': "#CDD1DE",
          'font_color': "#000000",
          'align': 'center',
          'valign': 'center',
          'text_wrap': True,
          'font_name': 'Calibri',
          'font_size': 10,
          'locked': 'True',
          'border': 4,
          'top': 4,
          'bottom': 4,
          'left': 4,
          'right': 4,	
          'border_color': "#FFFFFF",
          'num_format': 'dd.mm.yyyy'
      }
  )

  grayFormatLight = workbook.add_format(
      {
          'bg_color': "#E8E9EF",
          'font_color': "#000000",
          'align': 'center',
          'valign': 'center',
          'text_wrap': True,
          'font_name': 'Calibri',
          'font_size': 10,
          'locked': 'True',
          'border': 4,
          'top': 4,
          'bottom': 4,
          'left': 4,
          'right': 4,	
          'border_color': "#FFFFFF"
      }
  )

  grayFormatLightNum = workbook.add_format(
      {
          'bg_color': "#E8E9EF",
          'font_color': "#000000",
          'align': 'center',
          'valign': 'center',
          'text_wrap': True,
          'font_name': 'Calibri',
          'font_size': 10,
          'locked': 'True',
          'border': 4,
          'top': 4,
          'bottom': 4,
          'left': 4,
          'right': 4,	
          'border_color': "#FFFFFF",
          'num_format': 'dd.mm.yyyy'
      }
  )


  # Make the sheet white with no boarder.
  for whiteBackGroundCells in range(100): # integer odd-even alternation.
      main_worksheet.set_row(whiteBackGroundCells, cell_format=(whiteBackGroundFromat))

  # Set column width across the worksheet.
  main_worksheet.set_column("B:M", 21.57)

  # First all SSP merge cells.
  main_worksheet.merge_range('C2:M2', 'AWS', mergedFormat)

  # All headers and name of platform.
  main_worksheet.merge_range('B2:B4', 'SNAPSHOT ID', subMergedFormat)
  main_worksheet.merge_range('C3:C4', 'ENCRYPTED', subMergedFormat)
  main_worksheet.merge_range('D3:D4', 'DESCRIPTION', subMergedFormat)
  main_worksheet.merge_range('E3:E4', 'STARTED', subMergedFormat)
  main_worksheet.merge_range('F3:F4', 'VOLUME', subMergedFormat)
  main_worksheet.merge_range('G3:G4', 'VOLUME SIZE', subMergedFormat)
  main_worksheet.merge_range('H3:H4', 'VOLUME EXISTS', subMergedFormat)
  main_worksheet.merge_range('I3:I4', 'INSTANCE', subMergedFormat)
  main_worksheet.merge_range('J3:J4', 'INSTANCE NAME', subMergedFormat)
  main_worksheet.merge_range('K3:K4', 'INSTANCE EXISTS', subMergedFormat)
  main_worksheet.merge_range('L3:L4', 'AMI', subMergedFormat)
  main_worksheet.merge_range('M3:M4', 'AMI EXISTS', subMergedFormat)

  # Create a tupla to use later.
  return_tupla_to_later_reuse_temporal = workbook, grayFormatDark, grayFormatDarkNum, grayFormatLight, grayFormatLightNum

  # Return tupla
  return return_tupla_to_later_reuse_temporal


def write_in_excel_Worksheet(workbook, grayFormatDark, grayFormatDarkNum, grayFormatLight, grayFormatLightNum, data_information_complete):
  # We are going to LOAD previous Worksheet.
  existingWorksheet = workbook.get_worksheet_by_name('INFORMATION')

  row = 4
  col = 1

  # Loop to print to all rows and columns.
  for SnapshotId, Encrypted, Description, StartTime, VolumeId, VolumeSize, VolumeExists, Instance_id, Instance_name, Instance_exists, Image_id, Image_exists in data_information_complete:

      # Condition to format alternate rows.
      if row%2 == 1:
          cellFormatFix = grayFormatDark
          cellFormatNumFix = grayFormatDarkNum
      else:
          cellFormatFix = grayFormatLight
          cellFormatNumFix = grayFormatLightNum
      existingWorksheet.write_string(row, col, SnapshotId, cellFormatFix )
      existingWorksheet.write_string(row, col + 1 , Encrypted, cellFormatFix )
      existingWorksheet.write_string(row, col + 2 , Description, cellFormatFix )
      existingWorksheet.write_string(row, col + 3 , StartTime, cellFormatFix )
      existingWorksheet.write_string(row, col + 4 , VolumeId, cellFormatFix )
      existingWorksheet.write_string(row, col + 5 , VolumeSize, cellFormatFix )
      existingWorksheet.write_string(row, col + 6 , VolumeExists, cellFormatFix )
      existingWorksheet.write_string(row, col + 7 , Instance_id, cellFormatFix )
      existingWorksheet.write_string(row, col + 8 , Instance_name, cellFormatFix )
      existingWorksheet.write_string(row, col + 9 , Instance_exists, cellFormatFix )
      existingWorksheet.write_string(row, col + 10 , Image_id, cellFormatFix )
      existingWorksheet.write_string(row, col + 11 , Image_exists, cellFormatFix )
      row += 1

  workbook.close()
  print("Workbook closed")


def volume_exists(volume_id):
    if not volume_id: return ''
    try:
        ec2.describe_volumes(VolumeIds=[volume_id])
        return True
    except ClientError:
        return False


def instance_exists(instance_id):
    if not instance_id: return ''
    try:
        ec2.describe_instances(InstanceIds=[instance_id])
        return True
    except ClientError:
        return False


def image_exists(image_id):
    if not image_id: return ''
    try:
        ec2.describe_images(ImageIds=[image_id])
        return True
    except ClientError:
        return False


def get_all_snapshots():
    return ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']


def get_instance_name(ec2_instance_id):
    if not ec2_instance_id: return ''
    try:
        ec2 = boto3.client('ec2')
        ec2.describe_instances(InstanceIds=[ec2_instance_id])
        ec2 = boto3.resource('ec2')
        ec2instance = ec2.Instance(ec2_instance_id)
        for tags in ec2instance.tags:
            if tags["Key"] == 'Name':
                instancename = tags["Value"]
                return instancename
            else:
                return ''
    except ClientError:
        return ''


def parse_description(description):
    regex = r"^Created by CreateImage\((.*?)\) for (.*?) " # https://www.tutorialspoint.com/How-do-we-use-re-finditer-method-in-Python-regular-expression
    matches = re.finditer(regex, description, re.MULTILINE) # https://interactivechaos.com/en/python/function/remultiline
    for matchNum, match in enumerate(matches): # https://www.programiz.com/python-programming/methods/built-in/enumerate
        return match.groups()
    return '', ''


def obtain_all_results():
    global details
    details = []

    for snapshot in get_all_snapshots():
        iId, aMI = parse_description(snapshot['Description'])
        lsst = (f"{snapshot['SnapshotId']}|{snapshot['Encrypted']}|{snapshot['Description']}|{snapshot['StartTime']}|{snapshot['VolumeId']}|{snapshot['VolumeSize']}|{volume_exists(snapshot['VolumeId'])}|{iId}|{get_instance_name(iId)}|{instance_exists(iId)}|{iId}|{image_exists(aMI)}")
        details.append(lsst.split('|'))

    return details

# First execution.
data_information_complete = obtain_all_results()
# Create Excel and return tupla with all neccesary to later write with data.
return_tupla_to_later_reuse = create_excel(excelFileName)
# Write in an excel.
write_in_excel_Worksheet(return_tupla_to_later_reuse[0], return_tupla_to_later_reuse[1], return_tupla_to_later_reuse[2], return_tupla_to_later_reuse[3], return_tupla_to_later_reuse[4], data_information_complete)
