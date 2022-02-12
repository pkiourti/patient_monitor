# Project 2 - Patient Monitor Platform

## Database Schema

#### Users Table
- FristName
- LastName
- DateOfBirth
- Address
- State
- ZipCode
- PhoneNumber
- Email

#### Emergency Contact Table
- UserId
- EmergencyContactId

#### Roles Table
- Id
- Type (Patient, Family, Nurse, Doctor, Staff, Admin, Other)

#### RoleAssignment Table
- UserId
- RoleId
- CreatedAt

#### Measurements Type Table
- MeasurementId
- MeasurementName

#### Measurements Table
- UserId
- DeviceId
- MeasurementId
- Measurement
- CreatedAt
- UpdatedAt

#### Devices Type Table
- DeviceTypeId
- DeviceType

#### Devices
- Id
- DeviceTypeId
- Model
- PurchasedOn
- MACAddress
- SWVersion

#### DeviceAssignment Table
- Id 
- UserId
- AssignedBy
- AssignedAt
- UpdatedAt (will be used when the device was removed for that patient)
