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
                    onChangeText={(name) => props.oniFirstNameChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Last Name"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onLastNameChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Date of Birth"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onLastNameChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Address"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onLastNameChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="State"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onLastNameChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Zip code"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onLastNameChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Phone Number"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onLastNameChange(name)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Email"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(name) => props.onLastNameChange(name)}
                />
            </View>
            <TouchableOpacity
                style={styles.loginButton}
                onPress={() => props.onPress()}
            >
                <Text style={styles.loginText}>Register New User</Text>
            </TouchableOpacity>
          </View>
    )
};

const styles = StyleSheet.create({
    container: {
        flex: 10,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    textInput: {
        borderColor: '#18A8D8',
        borderRadius: 20,
        borderWidth: 1,
        width: "70%",
        height: 45,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 20,
    },
    registerButton: {
        alignItems: 'center',
        width: "40%",
        borderRadius: 10,
        height: 45,
        justifyContent: 'center',
        backgroundColor: '#18A8D8',
    },
    registerText: {
        color: '#FFF',
    },
});

export default RegisterUser;
