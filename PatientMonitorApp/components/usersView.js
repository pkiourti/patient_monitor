import React, { Component } from 'react';
import { StatusBar } from 'expo-status-bar';
import { ScrollView, StyleSheet, View, TextInput, TouchableOpacity, Alert } from 'react-native';

import { Table, TableWrapper, Row, Rows, Col, Cols, Cell } from 'react-native-table-component';

const UsersView = (props) => {
    const state = props.data
    return (
        <View style={styles.container}>
            <ScrollView horizontal={true}>
                <View>
                    <Table borderStyle={{borderWidth: 2, borderColor: '#C1C0B9'}}>
                        <Row data={state.tableHead} style={styles.head} textStyle={styles.text}/>
                        <Rows data={state.tableData} textStyle={styles.text} />
                    </Table>
                </View>
            </ScrollView>
        </View>
    )
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 16, paddingTop: 30, backgroundColor: '#fff' },
    head: { height: 40, backgroundColor: '#f1f8ff' },
    text: { minWidth: 100, margin: 6, textAlign: 'center' }
});

export default UsersView;
