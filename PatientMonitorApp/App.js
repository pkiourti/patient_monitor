import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import React, { Component } from 'react';
import { LoginPage, UsersView, RegisterUser, RegisterPatient } from './components';

export default class App extends Component {
    constructor(props) {
        super(props)

        this.onEmailChange = this.onEmailChange.bind(this)
        this.onPasswordChange = this.onPasswordChange.bind(this)
        this.getUsers = this.getUsers.bind(this)
        this.getPatients = this.getPatients.bind(this)
        this.onPress = this.onPress.bind(this)
        this.onFirstNameChange = this.onFirstNameChange.bind(this)
        this.onLastNameChange = this.onLastNameChange.bind(this)
        this.onDOBChange = this.onDOBChange.bind(this)
        this.onAddressChange = this.onAddressChange.bind(this)
        this.onStateChange = this.onStateChange.bind(this)
        this.onZipcodeChange = this.onZipcodeChange.bind(this)
        this.onUserEmailChange = this.onUserEmailChange.bind(this)
        this.onPhoneNumberChange = this.onPhoneNumberChange.bind(this)
        this.onPatientInfoChange = this.onPatientInfoChange.bind(this)
        this.onEmergencyContactChange = this.onEmergencyContactChange.bind(this)
        this.onViewRegisterUserPage = this.onViewRegisterUserPage.bind(this)
        this.onViewRegisterPatientPage = this.onViewRegisterPatientPage.bind(this)
        this.onGoBack = this.onGoBack.bind(this)
        this.onRegisterAUser = this.onRegisterAUser.bind(this)
        this.onRegisterAPatient = this.onRegisterAPatient.bind(this)
        this.state = {
            base_url: "https://b5d8-24-63-24-208.ngrok.io",
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

    getUsers() {
        fetch(this.state.base_url + "/users", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
        }).then(response =>
            response.json().then(data => {
                let values = data.map(item => [item.first_name, item.last_name, item.date_of_birth, item.address, item.state, item.zip_code, item.phone_number, item.email, item.created_at, item.updated_at])
                let head = ['First Name', 'Last Name', 'DOB', 'Address', 'State', 'Zip code', 'Phone Number', 'Email', 'Created', 'Updated']
                this.setState({usersHead: head, usersData: values, users: data})
            }).catch(error => {
                console.log(error)
            })
        ).catch(error => {
            console.log(error)
        });
    }

    getPatients() {
        fetch(this.state.base_url + "/patients", {
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

    componentDidMount() {
        this.getUsers()
        this.getPatients()
    }

    onEmailChange(email) {
        this.setState({email: email})
    }

    onPasswordChange(password) {
        this.setState({password: password})
    }

    onPress() {
        json_data = {"email": this.state.email, "password": this.state.password}
        fetch(this.state.base_url + "/auth", {
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
        if (this.state.viewRegisterUserPage) {
            this.setState({user: { ...this.state.user, first_name: name}})
        } else {
            this.setState({patient: { ...this.state.patient, first_name: name}})
        }
    }

    onLastNameChange(name) {
        if (this.state.viewRegisterUserPage) {
            this.setState({user: { ...this.state.user, last_name: name}})
        } else {
            this.setState({patient: { ...this.state.patient, last_name: name}})
        }
    }

    onDOBChange(name) {
        if (this.state.viewRegisterUserPage) {
            this.setState({user: { ...this.state.user, date_of_birth: name}})
        } else {
            this.setState({patient: { ...this.state.patient, date_of_birth: name}})
        }
    }

    onAddressChange(name) {
        if (this.state.viewRegisterUserPage) {
            this.setState({user: { ...this.state.user, address: name}})
        } else {
            this.setState({patient: { ...this.state.patient, address: name}})
        }
    }

    onStateChange(name) {
        if (this.state.viewRegisterUserPage) {
            this.setState({user: { ...this.state.user, state: name}})
        } else {
            this.setState({patient: { ...this.state.patient, state: name}})
        }
    }

    onZipcodeChange(name) {
        if (this.state.viewRegisterUserPage) {
            this.setState({user: { ...this.state.user, zipcode: name}})
        } else {
            this.setState({patient: { ...this.state.patient, zipcode: name}})
        }
    }

    onPhoneNumberChange(name) {
        if (this.state.viewRegisterUserPage) {
            this.setState({user: { ...this.state.user, phone_number: name}})
        } else {
            this.setState({patient: { ...this.state.patient, phone_number: name}})
        }
    }

    onUserEmailChange(name) {
        if (this.state.viewRegisterUserPage) {
            this.setState({user: { ...this.state.user, email: name}})
        } else {
            this.setState({patient: { ...this.state.patient, email: name}})
        }
    }

    onPatientInfoChange(name) {
        this.setState({patient: { ...this.state.patient, patient_history: name}})
    }

    onEmergencyContactChange(name) {
        this.setState({patient: { ...this.state.patient, emergency_contact_id: name}})
    }

    onGoBack() {
        this.setState({viewTables: true, viewRegisterUserPage: false})
    }

    onRegisterAUser() {
        fetch(this.state.base_url + "/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
            body: JSON.stringify({
                ...this.state.user,
            })
        }).then(response =>
            response.json().then(data => {
                /*var values = Object.keys(this.state.user).map((key) => { return this.state.user[key]; });*/
                /*this.setState({viewTables: true, viewRegisterUserPage: false, usersData: [ ...this.state.usersData, ...values ]})*/
                this.getUsers()
                this.setState({viewTables: true, viewRegisterUserPage: false})
            })
        ).catch(error => {
            Alert.alert('Something went wrong')
        });
    }

    onRegisterAPatient() {
        fetch(this.state.base_url + "/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
            body: JSON.stringify({
                ...this.state.patient,
            })
        }).then(response =>
            response.json().then(data => {
                fetch(this.state.base_url + "/patients", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/plain, */*",
                    },
                    body: JSON.stringify({
                        user_id: data.user_id,
                        emergency_contact_id: this.state.patient.emergency_contact_id ? this.state.patient.emergency_contact_id : this.state.users[0]._id,
                        patient_history: this.state.patient.patient_history,
                    })
                }).then(response =>
                    response.json().then(data => {
                        /*var values = Object.keys(this.state.user).map((key) => { return this.state.user[key]; });*/
                        /*this.setState({viewTables: true, viewRegisterUserPage: false, usersData: [ ...this.state.usersData, ...values ]})*/
                        this.getUsers()
                        this.getPatients()
                        this.setState({viewTables: true, viewRegisterPatientPage: false})
                    })
                ).catch(error => {
                    Alert.alert('Something went wrong')
                })
                /*var values = Object.keys(this.state.user).map((key) => { return this.state.user[key]; });*/
                /*this.setState({viewTables: true, viewRegisterUserPage: false, usersData: [ ...this.state.usersData, ...values ]})*/
            })
        ).catch(error => {
            Alert.alert('Something went wrong')
        });
    }

    onRegisterAUser() {
        fetch(this.state.base_url + "/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
            },
            body: JSON.stringify({
                ...this.state.user,
            })
        }).then(response =>
            response.json().then(data => {
                /*var values = Object.keys(this.state.user).map((key) => { return this.state.user[key]; });*/
                /*this.setState({viewTables: true, viewRegisterUserPage: false, usersData: [ ...this.state.usersData, ...values ]})*/
                this.getPatients()
                this.setState({viewTables: true, viewRegisterPatientPage: false})
            })
        ).catch(error => {
            Alert.alert('Something went wrong')
        });
    }

    render() {
        let page;
        if (this.state.viewLoginPage) {
            page = <LoginPage 
                onEmailChange={this.onEmailChange}
                onPasswordChange={this.onPasswordChange}
                onPress={this.onPress}
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
                        onRegisterAUser={this.onRegisterAUser}
                        onGoBack={this.onGoBack}
                    />
                </View>
        } else if (this.state.viewRegisterPatientPage) {
            page = <View>
                    <RegisterPatient 
                        users={this.state.users}
                        emergency_contact_id={this.state.patient.emergency_contact_id}
                        onFirstNameChange={this.onFirstNameChange}
                        onLastNameChange={this.onLastNameChange}
                        onDOBChange={this.onDOBChange}
                        onAddressChange={this.onAddressChange}
                        onStateChange={this.onStateChange}
                        onZipcodeChange={this.onZipcodeChange}
                        onPhoneNumberChange={this.onPhoneNumberChange}
                        onUserEmailChange={this.onUserEmailChange}
                        onEmergencyContactChange={this.onEmergencyContactChange}
                        onPatientInfoChange={this.onPatientInfoChange}
                        onRegisterAPatient={this.onRegisterAPatient}
                        onGoBack={this.onGoBack}
                    />
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
