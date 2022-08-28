import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import "./stylesheets/App.css";
import FormView from "./components/FormView";
import QuestionView from "./components/QuestionView";
import Header from "./components/Header";
import QuizView from "./components/QuizView";
import UserView from "./components/UserView";
import UserFormView from "./components/UserFormView";

class App extends Component {
  render() {
    return (
      <div className="App">
        <Header path />
        <Router>
          <Switch>
            <Route path="/" exact component={QuestionView} />
            <Route path="/add" component={FormView} />
            <Route path="/play" component={QuizView} />
            <Route path="/users" component={UserView} />
            <Route path="/add-user" component={UserFormView} />
            <Route component={QuestionView} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
