/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React, {useEffect, useState} from 'react';
import type {Node} from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  Text,
  useColorScheme,
  View,
  TextInput,
  Button,
} from 'react-native';
import Fili from 'fili';

import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-react-native/dist/platform_react_native';

const App: () => Node = () => {
  const isDarkMode = useColorScheme() === 'dark';

  const [tfReady, setTfReady] = useState(false);
  const [url, onChangeUrl] = React.useState('');
  const [finalData, setFinalData] = useState(0);
  // const [ratio, setRatio] = useState([]);
  // useEffect(() => {
  const urlSubmit = () => {
    let newUrl = url.replace(' ', '');
    const expressionWithHtml =
      /^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/;
    const expressionWithoutHtml =
      /^[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/;
    const expressionWithHtmlRegex = new RegExp(expressionWithHtml);
    const expressionWithoutHtmlRegex = new RegExp(expressionWithoutHtml);
    if (!newUrl.match(expressionWithHtmlRegex)) {
      if (!newUrl.match(expressionWithoutHtmlRegex)) {
        console.log('Bad Url');
        alert('Bad Url');
        return;
      } else {
        newUrl = 'http://' + newUrl;
      }
    }
    try {
      const ws = new WebSocket(newUrl);
      ws.onopen = e => {
        console.log('connected');
      };
      ws.onmessage = e => {
        // a message was received
        const data = e?.data;
        const finalData = parseFloat(data);
        console.log(finalData);
        setFinalData(finalData);
      };
    } catch (e) {
      console.log('Bad Url');
      alert('Bad Url');
      console.log(e);
    }
  };
  // useEffect(() => {
  //
  //   // const tfProcess = async () => {
  //   //   // await tf.setBackend('rn-webgl');
  //   //   await tf.ready();
  //   //   // Signal to the app that tensorflow.js can now be used.
  //   //   setTfReady(true);
  //   // };
  //   // tfProcess();
  // }, []);
  return (
    <SafeAreaView>
      <StatusBar barStyle={isDarkMode ? 'light-content' : 'dark-content'} />
      <ScrollView
        contentInsetAdjustmentBehavior="automatic"
        style={{height: '100%', margin: 24}}>
        <View>
          <Text>TensorFlow.js ready? {tfReady ? <Text>✅</Text> : ''}</Text>
        </View>
        <View>
          <TextInput
            onChangeText={onChangeUrl}
            value={url}
            style={{
              height: 40,
              margin: 12,
              borderWidth: 1,
              padding: 10,
              borderColor: '#000',
            }}
          />
        </View>
        <View>
          <Button title="Connect" onPress={urlSubmit} />
        </View>
        <View>
          <Text> Radius : {finalData ? finalData : ''}</Text>
        </View>
        <View
          style={{
            flex: 1,
            alignItems: 'center',
            marginTop: 300,
          }}>
          <View
            style={{
              borderRadius: 100,
              width: 100,
              height: 100,
              backgroundColor: 'red',
            }}
          />
          <View
            style={{
              borderRadius:
                100 + (finalData && typeof finalData === 'number' ? finalData : 0),
              width: 150 + (finalData && typeof finalData === 'number' ? finalData : 0),
              height: 150 + (finalData && typeof finalData === 'number' ? finalData : 0),
              marginTop:
                -125 - (finalData && typeof finalData === 'number' ? finalData : 0),
               zIndex: -1,
              backgroundColor: 'red',
            }}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default App;