import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import React, { Component } from 'react';
import { LoginPage, UsersView } from './components';

export default class App extends Component {
    constructor(props) {
        super(props)

        this.onEmailChange = this.onEmailChange.bind(this)
        this.onPasswordChange = this.onPasswordChange.bind(this)
        this.onPress = this.onPress.bind(this)
        this.fetchUsers = this.fetchUsers.bind(this)
        this.state = {
            viewLoginPage: true,
            email: '',
            password: '',
            selected: false,
            tableData: [],
            tableHead: [],
        }
    }

    onEmailChange(email) {
        this.setState({email: email})
    }

    onPasswordChange(password) {
        this.setState({password: password})
    }

    fetchUsers() {
        fetch("https://a51b-209-6-154-124.ngrok.io/users", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
        }).then(response =>
            response.json().then(data => {
                this.setState({tableHead: data["head"], tableData: data["data"], viewLoginPage: false})
            })
        ).catch(error => {
            console.log(error)
        });
    }

    onPress() {
        json_data = {"email": this.state.email, "password": this.state.password}
        fetch("https://a51b-209-6-154-124.ngrok.io/auth", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
        }).then(response =>
            response.json().then(data => {
                if (data == true) {
                    this.fetchUsers()
                }
            })
        ).catch(error => {
            console.log(error)
            Alert.alert()
        });
    }

    render() {
        return ( this.state.viewLoginPage ?
            <LoginPage 
                onEmailChange={this.onEmailChange}
                onPasswordChange={this.onPasswordChange}
                onPress={this.onPress}
                selected={this.selected}
            /> :
            <View style={styles.container}>
                <Text style={styles.text}>
                    Users Table
                </Text>
                <UsersView 
                    data={{"tableHead": this.state.tableHead, "tableData": this.state.tableData}}
                />
            </View>
        );
    }
};


const styles = StyleSheet.create({
    container: {
        marginBottom: 20,
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    text: {
        marginTop: 20,
    }
});
