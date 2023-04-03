import React, { useState, useEffect } from "react";
import FormContainer from "../FormContainer";
import { Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import Loader from "../Loader";
import Message from "../Message";
import  {register} from '../../actions/auth'
const RegisterScreen = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const userInfo = useSelector((state) => state.userLogin);
  const { loading, error, user } = userInfo;
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user]);
  const submitHandler = (e) => {
    e.preventDefault();
    if (password !== password2) {
      <Message variant="danger">Құпия сөз сәйкес емес</Message>;
    } else {
      console.log({ first_name:firstName, last_name:lastName, email, password1:password })
      dispatch(register({ first_name:firstName, last_name:lastName, email, password1:password }));
    }
  };
  return (
    <div>
      <FormContainer>
        <h1 className="py-3">Тіркелу</h1>
        <Form onSubmit={submitHandler}>
          {loading &&<Loader/>}
          {error ?  (
            typeof error =='string'?<Message variant="danger">{error}</Message>:error.map((err,i)=><Message variant="danger" key={i}>{err}</Message>)
          ) : <></>}

          <Form.Group className="mb-3">
            <Form.Label>Аты</Form.Label>
            <Form.Control
              type="text"
              required
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              placeholder="Атыңыз"
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Тегі</Form.Label>
            <Form.Control
              type="text"
              required
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder="Тегіңіз"
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Пошта</Form.Label>
            <Form.Control
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Пошта"
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Құпия сөз</Form.Label>
            <Form.Control
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Құпия сөз"
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Құпия сөз растау</Form.Label>
            <Form.Control
              type="password"
              required
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              placeholder="Құпия сөз растау"
            />
          </Form.Group>
          <Button variant="primary" type="submit">
            Тіркелу
          </Button>{" "}
          Аккаунтыңыз бар ма ?{" "}
          <Link
            style={{
              cursor: "pointer",
              textDecoration: "none",
              color: "black",
            }}
            to="/login"
          >
            Кіру
          </Link>
        </Form>
      </FormContainer>
    </div>
  );
};

export default RegisterScreen;
