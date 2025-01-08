import React, { useState } from 'react';
import { Card, Form, Button, Alert, Badge } from 'react-bootstrap';
import { Upload, X, Plus } from 'lucide-react';
import axios from 'axios';

const BotCreator = ({ onBotCreated }) => {
  const [botName, setBotName] = useState('');
  const [docs, setDocs] = useState([]);
  const [urls, setUrls] = useState(['']);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    setDocs([...docs, ...files]);
  };

  const removeDoc = (index) => {
    setDocs(docs.filter((_, i) => i !== index));
  };

  const handleUrlChange = (index, value) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  const addUrlField = () => {
    setUrls([...urls, '']);
  };

  const removeUrl = (index) => {
    setUrls(urls.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!botName.trim()) {
      setError('Bot name is required');
      return;
    }

    setIsLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('name', botName);
    docs.forEach((doc) => formData.append('documents', doc));
    urls.filter(url => url.trim()).forEach((url) => formData.append('urls', url));

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/create-bot', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onBotCreated(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create bot');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="shadow-sm">
      <Card.Body className="p-4">
        <h4 className="mb-4">Create New Bot</h4>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-4">
            <Form.Label>Bot Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter bot name"
              value={botName}
              onChange={(e) => setBotName(e.target.value)}
              required
            />
          </Form.Group>

          <Form.Group className="mb-4">
            <Form.Label>Upload Documentation Files</Form.Label>
            <div className="d-grid gap-2">
              <Button
                variant="outline-primary"
                className="d-flex align-items-center justify-content-center gap-2"
                as="label"
              >
                <Upload size={20} />
                Choose Files
                <Form.Control
                  type="file"
                  hidden
                  multiple
                  onChange={handleFileUpload}
                  accept=".pdf,.doc,.docx,.txt,.md"
                />
              </Button>
            </div>
            <div className="mt-3 d-flex flex-wrap gap-2">
              {docs.map((doc, index) => (
                <Badge 
                  bg="light" 
                  text="dark" 
                  className="d-flex align-items-center p-2"
                  key={index}
                >
                  {doc.name}
                  <X
                    size={16}
                    className="ms-2 cursor-pointer"
                    onClick={() => removeDoc(index)}
                  />
                </Badge>
              ))}
            </div>
          </Form.Group>

          <Form.Group className="mb-4">
            <Form.Label>Documentation URLs</Form.Label>
            {urls.map((url, index) => (
              <div key={index} className="d-flex gap-2 mb-2">
                <Form.Control
                  type="url"
                  placeholder="Enter documentation URL"
                  value={url}
                  onChange={(e) => handleUrlChange(index, e.target.value)}
                />
                <Button
                  variant="outline-danger"
                  onClick={() => removeUrl(index)}
                >
                  <X size={20} />
                </Button>
              </div>
            ))}
            <Button
              variant="outline-secondary"
              className="d-flex align-items-center gap-2"
              onClick={addUrlField}
              type="button"
            >
              <Plus size={20} />
              Add URL
            </Button>
          </Form.Group>

          {error && (
            <Alert variant="danger" className="mb-4">
              {error}
            </Alert>
          )}

          <div className="d-grid">
            <Button
              type="submit"
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? 'Creating Bot...' : 'Create Bot'}
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default BotCreator; 