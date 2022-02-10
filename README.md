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
- MeasurementId
- Measurement
- CreatedAt

#### Devices Type Table
- DeviceId
- DeviceType

#### Devices
- Id
- DeviceId
- Model
- PurchasedOn
- MACAddress
- SWVersion

#### DeviceAssignment Table
- Id 
- UserId
- AssignedAt
- AssignedBy
- UpdatedAt (will be when the device was removed for that patient)
