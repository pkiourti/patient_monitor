import React, { Component } from 'react';
import { StatusBar } from 'expo-status-bar';
import { ScrollView, StyleSheet, Text, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import {Picker} from '@react-native-picker/picker';

const RegisterPatient = (props) => {
    return (
        <ScrollView style={styles.scrollView}>
          <View style={styles.container}>
            <StatusBar style="auto" />
            <View style={styles.textInput}>
                <TextInput
                    placeholder="First Name"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(fname) => props.onFirstNameChange(fname)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Last Name"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(lname) => props.onLastNameChange(lname)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Date of Birth"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onDOBChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Address"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onAddressChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="State"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onStateChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Zip code"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onZipcodeChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Phone Number"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onPhoneNumberChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Email"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onUserEmailChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Patient History"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onPatientInfoChange(name)}
                />
            </View>
            <View style={styles.dropDown}>
              <Picker
                style={{ height: 50, width: "100%", color: '#18A8D8'}}
                placeholder="Select Emergency Contact" 
                selectedValue={props.emergency_contact_id}
                onValueChange={(itemValue, itemIndex) => props.onEmergencyContactChange(itemValue)}
              >
                {props.users.length > 0 && props.users.map((item) =>
                    <Picker.Item key={item._id} label={"Emergency Contact: " + item.first_name + " " + item.last_name} value={item._id} />
                 )}
              </Picker>
            </View>
            <TouchableOpacity
                style={styles.registerButton}
                onPress={() => props.onRegisterAPatient()}
            >
                <Text style={styles.registerText}>Register Patient</Text>
            </TouchableOpacity>
            <TouchableOpacity
                style={styles.registerButton}
                onPress={() => props.onGoBack()}
            >
                <Text style={styles.registerText}>Go Back</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
    )
};

const styles = StyleSheet.create({
    container: {
        backgroundColor: '#fff',
        alignItems: 'center',
        marginTop: 20,
    },
    textInput: {
        borderColor: '#18A8D8',
        borderRadius: 20,
        borderWidth: 1,
        width: "70%",
        height: 45,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 10,
        marginTop: 10,
    },
    dropDown: {
        borderColor: '#18A8D8',
        borderRadius: 20,
        borderWidth: 1,
        width: "70%",
        height: 45,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 10,
        marginTop: 10,
    },
    registerButton: {
        alignItems: 'center',
        width: "40%",
        borderRadius: 15,
        height: 45,
        justifyContent: 'center',
        backgroundColor: '#18A8D8',
        marginTop: 10,
        marginBottom: 10,
    },
    registerText: {
        color: '#FFF',
    },
});

export default RegisterPatient;
