import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import React, { Component } from 'react';
import { LoginPage, UsersView, RegisterUser } from './components';

export default class App extends Component {
    constructor(props) {
        super(props)

        this.onEmailChange = this.onEmailChange.bind(this)
        this.onPasswordChange = this.onPasswordChange.bind(this)
        this.onPress = this.onPress.bind(this)
        this.onFirstNameChange = this.onFirstNameChange.bind(this)
        this.onLastNameChange = this.onLastNameChange.bind(this)
        this.onDOBChange = this.onDOBChange.bind(this)
        this.onAddressChange = this.onAddressChange.bind(this)
        this.onStateChange = this.onStateChange.bind(this)
        this.onZipcodeChange = this.onZipcodeChange.bind(this)
        this.onUserEmailChange = this.onUserEmailChange.bind(this)
        this.onPhoneNumberChange = this.onPhoneNumberChange.bind(this)
        this.onViewRegisterUserPage = this.onViewRegisterUserPage.bind(this)
        this.onViewRegisterPatientPage = this.onViewRegisterPatientPage.bind(this)
        this.state = {
            viewLoginPage: true,
            viewTables: false,
            viewRegisterUserPage: false,
            viewRegisterPatientPage: false,
            email: '',
            password: '',
            selected: false,
            usersHead: [],
            usersData: [],
            patientsHead: [],
            patientsData: [],
            user: {},
            patient: {}
        }
    }

    componentDidMount() {
        fetch("https://74e1-155-41-14-29.ngrok.io/users", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
        }).then(response =>
            response.json().then(data => {
                this.setState({usersHead: data["head"], usersData: data["data"]})
            })
        ).catch(error => {
            console.log(error)
        });
        fetch("https://74e1-155-41-14-29.ngrok.io/patients", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
        }).then(response =>
            response.json().then(data => {
                this.setState({patientsHead: data["head"], patientsData: data["data"]})
            })
        ).catch(error => {
            console.log(error)
        });
    }

    onEmailChange(email) {
        this.setState({email: email})
    }

    onPasswordChange(password) {
        this.setState({password: password})
    }

    onPress() {
        json_data = {"email": this.state.email, "password": this.state.password}
        fetch("https://74e1-155-41-14-29.ngrok.io/auth", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
            body: JSON.stringify({
                email: this.state.email,
                password: this.state.password,
            })
        }).then(response =>
            response.json().then(data => {
                if (data == true) {
                    this.setState({viewLoginPage: false, viewTables: true})
                } else {
                    Alert.alert('Wrong Email or Password')
                }
            })
        ).catch(error => {
            Alert.alert('Something went wrong')
        });
    }

    onViewRegisterUserPage() {
        this.setState({viewTables: false, viewRegisterUserPage: true})
    }

    onViewRegisterPatientPage() {
        this.setState({viewTables: false, viewRegisterPatientPage: true})
    }

    onFirstNameChange(name) {
        this.setState({user: {...this.state.user, "firstName": name}})
    }

    onLastNameChange(name) {
        this.setState({user: {...this.state.user, "lastName": name}})
    }

    onDOBChange(name) {
        this.setState({user: {...this.state.user, "dob": name}})
    }

    onAddressChange(name) {
        this.setState({user: {...this.state.user, "address": name}})
    }

    onStateChange(name) {
        this.setState({user: {...this.state.user, "state": name}})
    }

    onZipcodeChange(name) {
        this.setState({user: {...this.state.user, "zipcode": name}})
    }

    onPhoneNumberChange(name) {
        this.setState({user: {...this.state.user, "phoneNumber": name}})
    }

    onUserEmailChange(name) {
        this.setState({user: {...this.state.user, "email": name}})
    }


    render() {
        let page;
        if (this.state.viewLoginPage) {
            page = <LoginPage 
                onEmailChange={this.onEmailChange}
                onPasswordChange={this.onPasswordChange}
                onPress={this.onPress}
                selected={this.selected}
            />
        } else if (this.state.viewTables) {
            page = <View style={styles.container}>
                <Text style={styles.text}>
                    Users Table
                </Text>
                <UsersView 
                    data={{"tableHead": this.state.usersHead, "tableData": this.state.usersData}}
                />
                <TouchableOpacity
                    style={styles.registerButton}
                    onPress={() => this.onViewRegisterUserPage()}
                >
                    <Text style={styles.registerText}>Register a User</Text>
                </TouchableOpacity>
                <Text style={styles.text}>
                    Patients Table
                </Text>
                <UsersView 
                    data={{"tableHead": this.state.patientsHead, "tableData": this.state.patientsData}}
                />
                <TouchableOpacity
                    style={styles.registerButton}
                    onPress={() => this.onViewRegisterPatientPage()}
                >
                    <Text style={styles.registerText}>Register a Patient</Text>
                </TouchableOpacity>
            </View>
        } else if (this.state.viewRegisterUserPage) {
            page = <View>
                    <RegisterUser 
                        onFirstNameChange={this.onFirstNameChange}
                        onLastNameChange={this.onLastNameChange}
                        onDOBChange={this.onDOBChange}
                        onAddressChange={this.onAddressChange}
                        onStateChange={this.onStateChange}
                        onZipcodeChange={this.onZipcodeChange}
                        onPhoneNumberChange={this.onPhoneNumberChange}
                        onUserEmailChange={this.onUserEmailChange}
                    />
                    <TouchableOpacity
                        style={styles.registerButton}
                        onPress={() => this.setState({viewTables: true, viewRegisterUserPage: false})}
                    >
                        <Text style={styles.registerText}>Go back</Text>
                    </TouchableOpacity>
                </View>
        } else if (this.state.viewRegisterPatientPage) {
            page = <View>
                    <Text>Register a Patient</Text>
                    <TouchableOpacity
                        style={styles.registerButton}
                        onPress={() => this.setState({viewTables: true, viewRegisterPatientPage: false})}
                    >
                        <Text style={styles.registerText}>Go back</Text>
                    </TouchableOpacity>
                </View>
        }
        return (
            page
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
