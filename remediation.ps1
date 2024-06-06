#Disable Bluetooth File Transfer
#Remediation Script
#22.10.15
$Compliance = "Compliant"
$TargetServicesAllowedList = "{0000111E-0000-1000-8000-00805F9B34FB};{00001203-0000-1000-8000-00805F9B34FB};{00001108-0000-1000-8000-00805F9B34FB};{00001200-0000-1000-8000-00805F9B34FB};{0000110B-0000-1000-8000-00805F9B34FB};{0000110C-0000-1000-8000-00805F9B34FB};{0000110E-0000-1000-8000-00805F9B34FB};{0000110F-0000-1000-8000-00805F9B34FB};{00001124-0000-1000-8000-00805F9B34FB};{00001801-0000-1000-8000-00805F9B34FB};{00001812-0000-1000-8000-00805F9B34FB};{00001800-0000-1000-8000-00805F9B34FB};{0000180A-0000-1000-8000-00805F9B34FB};{00001813-0000-1000-8000-00805F9B34FB};{00002a04-0000-1000-8000-00805f9b34fb};{00002a00-0000-1000-8000-00805f9b34fb};{00002a01-0000-1000-8000-00805f9b34fb};{00002a05-0000-1000-8000-00805f9b34fb};{00002a29-0000-1000-8000-00805f9b34fb};{00002a24-0000-1000-8000-00805f9b34fb};{00002a25-0000-1000-8000-00805f9b34fb};{00002a27-0000-1000-8000-00805f9b34fb};{00002a26-0000-1000-8000-00805f9b34fb};{00002a28-0000-1000-8000-00805f9b34fb};{00002a23-0000-1000-8000-00805f9b34fb};{00002a2a-0000-1000-8000-00805f9b34fb};{00002a50-0000-1000-8000-00805f9b34fb};{0000180f-0000-1000-8000-00805f9b34fb};{00002a19-0000-1000-8000-00805f9b34fb};{0000ae40-0000-1000-8000-00805f9b34fb};{0000ae41-0000-1000-8000-00805f9b34fb};{0000ae42-0000-1000-8000-00805f9b34fb};{00002A4E-0000-1000-8000-00805f9b34fb};{00002A4D-0000-1000-8000-00805f9b34fb};{00002A4B-0000-1000-8000-00805f9b34fb};{00002A4A-0000-1000-8000-00805f9b34fb};{00002A4C-0000-1000-8000-00805f9b34fb};{00002A33-0000-1000-8000-00805f9b34fb}"
$CurrentServicesAllowedList = (Get-CimInstance -Namespace 'root\cimv2\mdm\dmmap' -Query 'Select * from MDM_Policy_Result01_Bluetooth02').ServicesAllowedList

if ($CurrentServicesAllowedList -ne $TargetServicesAllowedList)
{
    $Compliance = "Non-compliant"
}

if ($Compliance = "Non-compliant") {
    #Check for Instance
    $BluetoothPolicy = Get-CimInstance -Namespace 'root\cimv2\mdm\dmmap' -Query 'Select * from MDM_Policy_Config01_Bluetooth02'

    #Turn off Bluetooth file transfer
    #If Bluetooth policy exists then set ServicesAllowedList
    if ($BluetoothPolicy)
    {
        $Result = Set-CimInstance -InputObject $BluetoothPolicy -Property @{ParentID="./Vendor/MSFT/Policy/Config";InstanceID="Bluetooth";ServicesAllowedList=$TargetServicesAllowedList}
    }
    #If Bluetooth policy does not exist then create it and set ServicesAllowedList
    else {
        $Result = New-CimInstance -Namespace 'root\cimv2\mdm\dmmap' -ClassName 'MDM_Policy_Config01_Bluetooth02' -Property @{ParentID="./Vendor/MSFT/Policy/Config";InstanceID="Bluetooth";ServicesAllowedList=$TargetServicesAllowedList}
    }
}
Exit $Result.ReturnValue
