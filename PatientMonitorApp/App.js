import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import React, { Component } from 'react';
import { LoginPage } from './components';

export default class App extends Component {
    constructor(props) {
        super(props)

        this.onEmailChange = this.onEmailChange.bind(this)
        this.onPasswordChange = this.onPasswordChange.bind(this)
        this.onPress = this.onPress.bind(this)
        this.state = {
            base: "https://a51b-209-6-154-124.ngrok.io/",
            viewLoginPage: true,
            email: '',
            password: '',
            selected: false
        }
    }

    onEmailChange(email) {
        this.setState({email: email})
    }

    onPasswordChange(password) {
        this.setState({password: password})
    }

    onPress() {
        json_data = {"email": this.state.email, "password": this.state.password}
        fetch(this.state.base + 'auth', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(json_data)
        }).then(response =>
            response.json().then(data => {
                if (data == true) {
                    this.setState({viewLoginPage: false})
                }
            })
        ).catch(error => {
            console.log(error)
            Alert.alert()
        });
    }

    render() {
        return (
            <LoginPage 
                onEmailChange={this.onEmailChange}
                onPasswordChange={this.onPasswordChange}
                onPress={this.onPress}
                selected={this.selected}
            />
        );
    }
};
