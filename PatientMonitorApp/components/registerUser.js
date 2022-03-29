import React, { Component } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Alert } from 'react-native';

const RegisterUser = (props) => {
    return (
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
            <TouchableOpacity
                style={styles.registerButton}
                onPress={() => props.onRegisterAUser()}
            >
                <Text style={styles.registerText}>Register User</Text>
            </TouchableOpacity>
            <TouchableOpacity
                style={styles.registerButton}
                onPress={() => props.onGoBack()}
            >
                <Text style={styles.registerText}>Go Back</Text>
            </TouchableOpacity>
          </View>
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

export default RegisterUser;
