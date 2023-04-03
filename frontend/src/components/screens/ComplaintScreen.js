import React, { useState, useEffect } from "react";
import {
  Form,
  Row,
  Col,
  FloatingLabel,
  Button,
  Figure,
  Image,
} from "react-bootstrap";
import Loader from "../Loader";
import { useDispatch, useSelector } from "react-redux";
import { Navigate, useLocation } from "react-router";
import { useNavigate } from "react-router";
import { getCategories } from "../../actions/categoryActions";
import { getNeighborhoods } from "../../actions/neighborhood";
import {
  addComplaint,
  getMyComplaintById,
  updateComplaint,
} from "../../actions/complaintActions";
import Message from "../Message";
import axios from "axios";
const ComplaintScreen = () => {
  const location = useLocation();
  const id = location.search ? location.search.split("=")[1] : "";
  const [message, setMessage] = useState("");
  const [topicState, setTopicState] = useState("");
  const [descriptionState, setDescriptionState] = useState("");
  const [subCategoryState, setSubCategoryState] = useState("");
  const [neighborhoodState, setNeighborhoodState] = useState("");
  const [contactEmailState, setContactEmailState] = useState("");
  const [contactNumberState, setContactNumberState] = useState("");
  const [isAnonymous, setIsAnonymous] = useState(false);
  const [image, setImage] = useState("");
  const [uploading, setUploading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const {
    category,
    loading: categoryLoading,
    error: categoryError,
  } = useSelector((state) => state.category);
  const {
    complaint,
    loading: getComplaintLoading,
    error: getComplaintError,
  } = useSelector((state) => state.getComplaintById);
  const {
    neighborhood,
    loading: neighborhoodLoading,
    error: neighborhoodError,
  } = useSelector((state) => state.neighborhood);
  const {
    user,
    loading: userLoading,
    error: userError,
  } = useSelector((state) => state.userLogin);
  const { success: addedComplaint } = useSelector(
    (state) => state.addComplaint
  );
  useEffect(() => {
    if (id && complaint && complaint.topic) {
      setTopicState(!getComplaintLoading && complaint.topic);
      setDescriptionState(complaint.description);
      setImage(complaint.img == null ? "" : complaint.img);
      setNeighborhoodState(complaint.neighborhood && complaint.neighborhood.id);
      setSubCategoryState(complaint.sub_category.id);

      setContactNumberState(complaint.contact.phone);
      setContactEmailState(complaint.contact.email);
    }
  }, [complaint]);
  useEffect(() => {
    if (!user) {
      navigate("/");
    } else if (!category || !neighborhood) {
      dispatch(getCategories());
      dispatch(getNeighborhoods());
    }
    if (id) {
      dispatch(getMyComplaintById(id));
    }
    if (complaint && complaint.id == id) {
      console.log("equal");
    }
  }, [dispatch, user, id]);
  const submitHandler = (e) => {
    e.preventDefault();
    setMessage("");
    if (
      !descriptionState ||
      !topicState ||
      !subCategoryState ||
      !neighborhoodState
    ) {
      setMessage("Please fill in all flields");
    } else {
      let form = null;
      if (!isAnonymous) {
        form = {
          description: descriptionState,
          topic: topicState,
          category_id: subCategoryState,
          neighborhood_id: neighborhoodState,
          contact: {
            email: contactEmailState,
            phone: contactNumberState,
          },
        };
      } else {
        form = {
          description: descriptionState,
          topic: topicState,
          category_id: subCategoryState,
          neighborhood_id: neighborhoodState,
          contact: {
            email: "",
            phone: "",
          },
        };
      }
      if (id) {
        dispatch(updateComplaint(id, form));
        setMessage("Complaint updated successfully!");
        scrollToTop();
        setTimeout(() => {
          navigate("/profile");
        }, 2000);
      } else {
        dispatch(addComplaint(form));
        scrollToTop();
        setTimeout(() => {
          navigate("/profile");
        }, 2000);
      }
    }
  };
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth", // for smoothly scrolling
    });
  };
  const uploadImageHandler = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("image", file);
    setUploading(true);

    try {
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      const { data } = await axios.post(`/api/upload/${id}`, formData, config);
      console.log(data);
      setImage(data);
      setUploading(false);
    } catch (error) {
      console.error(error);
      setUploading(false);
    }
  };
  return (
    <div>
      <h1 className="text-center">
        {id ? "Шағым өзгерту" : "Шағым жіберу"}
      </h1>
      <Form onSubmit={submitHandler}>
        <Row className="justify-content-center">
          <Col md={8}>
            {message != "" && (
              <Message id="alert" variant={"success"}>
                {message}
              </Message>
            )}
            {addedComplaint && (
              <Message id="alert" variant="success">
                Шағым жіберілді!
              </Message>
            )}
            <p className="lead">Шағым детальдары</p>
            <FloatingLabel
              controlId="floatingInput1"
              label="Шағымның қысқаша сипаттамасы"
              className="mb-3"
            >
              <Form.Control
                type="text"
                placeholder="Шағымның қысқаша тақырыбы "
                value={topicState}
                onChange={(e) => setTopicState(e.target.value)}
                required
              />
            </FloatingLabel>
          </Col>
        </Row>
        <Row className="justify-content-center">
          <Col md={8}>
            <FloatingLabel
              controlId="floatingTextarea2"
              label="Шағымның толық сипаттамасы"
              className="mb-3"
            >
              <Form.Control
                as="textarea"
                style={{ height: "100px" }}
                placeholder="Шағымның толық сипаттамасы"
                value={descriptionState}
                onChange={(e) => setDescriptionState(e.target.value)}
                required
              />
            </FloatingLabel>
            {id && (
              <Row>
                <Col>
                  <Form.Group controlId="formFile3" className="mb-3">
                    <Form.Label>Сурет (міндетті емес)</Form.Label>
                    <Form.Control
                      type="file"
                      id="image-file"
                      label={image}
                      onChange={(e) => uploadImageHandler(e)}
                    />
                  </Form.Group>
                </Col>
                <Col>
                  {uploading && <Loader />}
                  {image != "" && (
                    <Image
                      src={image}
                      rounded
                      fluid
                      style={{ width: "100%", height: "100%" }}
                    />
                  )}
                </Col>
              </Row>
            )}
          </Col>
        </Row>
        <Row className="justify-content-center py-3">
          <Col md={8}>
            <p className="lead">Шағым қатысты</p>
            <Form.Select
              aria-label="Floating label select example"
              value={neighborhoodState}
              onChange={(e) => setNeighborhoodState(e.target.value)}
              required
            >
              <option>Ауданды таңдаңыз</option>
              {neighborhood &&
                neighborhood.map((neighborhood) => (
                  <option key={neighborhood.id} value={neighborhood.id}>
                    {neighborhood.name}
                  </option>
                ))}
            </Form.Select>
          </Col>
        </Row>
        <Row className="justify-content-center py-3">
          <Col md={8}>
            <Form.Select
              aria-label="Floating label select example"
              value={subCategoryState}
              onChange={(e) => setSubCategoryState(e.target.value)}
              required
            >
              <option>Категорияны таңдаңыз</option>
              {category &&
                category.map(({ id, category, sub_categories }) => {
                  return (
                    <>
                      <option
                        key={id}
                        disabled
                        style={{ color: "black", fontWeight: "300" }}
                      >
                        *{category}*
                      </option>
                      {sub_categories[0] != null &&
                        sub_categories.map((sub) => (
                          <option key={100 * id + sub.id} value={sub.id}>
                            {sub.sub_category}
                          </option>
                        ))}
                    </>
                  );
                })}
            </Form.Select>
          </Col>
        </Row>
        <Row className="justify-content-center py-3">
          <Col md={8}>
            <p className="text-center lead">
              Анонимді шағым жауапсыз,ұсыныс ретінде қарастырылады
            </p>
            <Form.Group className="mb-3" controlId="formBasicCheckbox4">
              <Form.Check
                label="Анонимді"
                type="checkbox"
                className="py-3"
                checked={isAnonymous}
                onChange={(e) => setIsAnonymous(e.target.checked)}
              />
            </Form.Group>
          </Col>
        </Row>
        <Row className="justify-content-center py-3">
          <p className="text-center lead">
            Міндетті емес, егерде пошта немесе телефон номеры арқылы жауап алғыңыз келмесе
          </p>
          <Col md={4}>
            <p className="lead">Хабарласу поштасы</p>
            <Form.Group className="mb-3" controlId="formBasicEmail5">
              <Form.Control
                disabled={isAnonymous}
                type="email"
                placeholder={
                  isAnonymous ? "Анонимді болса, міндетті емес" : "Пошта енгізіңіз"
                }
                value={contactEmailState}
                onChange={(e) => setContactEmailState(e.target.value)}
              />
            </Form.Group>
          </Col>
          <Col md={4}>
            <p className="lead">Хабарласу нөмірі</p>
            <Form.Group className="mb-3" controlId="formBasicEmail6">
              <Form.Control
                type="text"
                disabled={isAnonymous}
                placeholder={
                  isAnonymous ? "Анонимді болса, міндетті емес" : "Нөмір енгізіңіз"
                }
                value={contactNumberState}
                onChange={(e) => setContactNumberState(e.target.value)}
              />
            </Form.Group>
          </Col>
        </Row>
        <Row className="justify-content-center">
          <Col md={8}>
            <Button type="submit">{id ? "Өзгерту" : "Жіберу"}</Button>
          </Col>
        </Row>
      </Form>
    </div>
  );
};

export default ComplaintScreen;
