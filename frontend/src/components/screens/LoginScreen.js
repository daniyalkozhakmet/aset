import React, { useState, useEffect } from "react";
import FormContainer from "../FormContainer";
import { Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../../actions/auth";
import Message from "../Message";
import Loader from "../Loader";

const LoginScreen = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const userInfo = useSelector((state) => state.userLogin);
  const { loading, error, user } = userInfo;
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const submitHandler = (e) => {
    e.preventDefault();
    console.log({ email, password });
    dispatch(login({ email, password }));
  };
  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user]);
  return (
    <div>
      <FormContainer>
        <h1 className="py-3">Кіру</h1>
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <></>
        )}
        <Form onSubmit={submitHandler}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Пошта</Form.Label>
            <Form.Control
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter email"
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Құпия сөз</Form.Label>
            <Form.Control
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter email"
            />
          </Form.Group>
          <Button variant="primary" type="submit">
            Кіру
          </Button>{" "}
          Аккаунтыңыз жоқ па?{" "}
          <Link
            style={{
              cursor: "pointer",
              textDecoration: "none",
              color: "black",
            }}
            to="/register"
          >
            Тіркелу
          </Link>
        </Form>
      </FormContainer>
    </div>
  );
};

export default LoginScreen;
