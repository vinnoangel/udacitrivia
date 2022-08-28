import React, { Component } from "react";
import "../stylesheets/Question.css";

const starArray = [5, 4, 3, 2, 1];

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  createStars(rating, id) {
    return (
      <div className="rating">
        {starArray.map((num) => (
          <div
            key={num}
            // onClick={() => {
            //   this.changeRating(id, num);
            // }}
            className={`star ${rating >= num ? "active" : ""}`}
          />
        ))}
      </div>
    );
  }

  render() {
    const { question, answer, category, difficulty, rating, id } = this.props;
    console.log(category);
    return (
      <div className="Question-holder">
        <div className="Question">{question}</div>
        <div className="Question-status">
          <img
            className="category"
            alt={`${category.toLowerCase()}`}
            src={`${category.toLowerCase()}.svg`}
          />
          <div className="difficulty">Difficulty: {difficulty}</div>
          <img
            src="delete.png"
            alt="delete"
            className="delete"
            title="Delete Question"
            onClick={() => this.props.questionAction("DELETE")}
          />
        </div>
        {this.createStars(rating, id)}
        <div
          className="show-answer button"
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? "Hide" : "Show"} Answer
        </div>
        <div className="answer-holder">
          <span
            style={{
              visibility: this.state.visibleAnswer ? "visible" : "hidden",
            }}
          >
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
