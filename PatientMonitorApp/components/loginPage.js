import React, { Component } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Alert } from 'react-native';

const LoginPage = (props) => {
    return (
          <View style={styles.container}>
            <StatusBar style="auto" />
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Email"
                    placeholderTextColor="#18A8D8"
                    onChangeText={(email) => props.onEmailChange(email)}
                />
            </View>
            <View style={styles.textInput}>
                <TextInput
                    placeholder="Password"
                    placeholderTextColor="#18A8D8"
                    secureTextEntry={true}
                    onChangeText={(password) => props.onPasswordChange(password)}
                />
            </View>
            <TouchableOpacity
                style={styles.loginButton}
                onPress={() => props.onPress()}
            >
                <Text style={styles.loginText}>Login</Text>
            </TouchableOpacity>
          </View>
    )
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
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
    loginButton: {
        alignItems: 'center',
        width: "20%",
        borderRadius: 10,
        height: 35,
        justifyContent: 'center',
        backgroundColor: '#18A8D8',
    },
    loginText: {
        color: '#FFF',
    },
});

export default LoginPage;
