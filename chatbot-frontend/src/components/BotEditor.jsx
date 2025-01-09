import React, { useState } from 'react';
import { Card, Form, Button, Alert, Badge, Spinner } from 'react-bootstrap';
import { Upload, X, Plus } from 'lucide-react';
import axios from 'axios';

const BotEditor = ({ bots, onBotUpdated, onSelectBot }) => {
  const [selectedBot, setSelectedBot] = useState(null);
  const [botName, setBotName] = useState('');
  const [docs, setDocs] = useState([]);
  const [urls, setUrls] = useState(['']);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleBotSelect = (bot) => {
    setSelectedBot(bot);
    setBotName(bot.name);
    setDocs(bot.documents || []);
    setUrls(bot.urls || ['']);
    onSelectBot(bot);
  };

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
    if (!selectedBot) {
      setError('Please select a bot to update');
      return;
    }
    if (!botName.trim()) {
      setError('Bot name is required');
      return;
    }

    setIsLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('name', botName);
    formData.append('botId', selectedBot.id);
    docs.forEach((doc) => formData.append('documents', doc));
    urls.filter(url => url.trim()).forEach((url) => formData.append('urls', url));

    try {
      const response = await axios.put('http://127.0.0.1:5000/api/update-bot', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onBotUpdated(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update bot');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="border-0 bg-transparent">
      <Card.Body className="p-0">
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-4">
            <Form.Label className="fw-semibold">Select Assistant to Update</Form.Label>
            <Form.Select 
              value={selectedBot?.id || ''} 
              onChange={(e) => {
                const bot = bots.find(b => b.id === e.target.value);
                handleBotSelect(bot);
              }}
            >
              <option value="">Choose an assistant...</option>
              {bots.map(bot => (
                <option key={bot.id} value={bot.id}>{bot.name}</option>
              ))}
            </Form.Select>
          </Form.Group>

          {selectedBot && (
            <>
              <div className="mb-4 pb-3 border-bottom">
                <Form.Group>
                  <Form.Label className="fw-semibold mb-2">Bot Name</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter a name for your bot"
                    value={botName}
                    onChange={(e) => setBotName(e.target.value)}
                    required
                    className="form-control-lg"
                  />
                </Form.Group>
              </div>

              <Form.Group className="mb-4">
                <Form.Label className="fw-semibold mb-3">Documentation Files</Form.Label>
                <div className="upload-zone p-4 text-center bg-light rounded-3 mb-3">
                  <Button
                    variant="primary"
                    className="d-inline-flex align-items-center gap-2 mb-2"
                    as="label"
                  >
                    <Upload size={20} />
                    Add More Files
                    <Form.Control
                      type="file"
                      hidden
                      multiple
                      onChange={handleFileUpload}
                      accept=".pdf,.doc,.docx,.txt,.md"
                    />
                  </Button>
                  <div className="text-muted small">
                    Supported formats: PDF, DOC, DOCX, TXT, MD
                  </div>
                </div>
                {docs.length > 0 && (
                  <div className="selected-files p-3 bg-white rounded-3 border">
                    <div className="small fw-semibold mb-2">Current Files:</div>
                    <div className="d-flex flex-wrap gap-2">
                      {docs.map((doc, index) => (
                        <Badge 
                          bg="light" 
                          text="dark" 
                          className="d-flex align-items-center p-2"
                          key={index}
                        >
                          {doc.name}
                          <X
                            size={14}
                            className="ms-2 cursor-pointer"
                            onClick={() => removeDoc(index)}
                          />
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </Form.Group>

              <Form.Group className="mb-4">
                <Form.Label className="fw-semibold mb-3">Documentation URLs</Form.Label>
                <div className="url-inputs">
                  {urls.map((url, index) => (
                    <div key={index} className="d-flex gap-2 mb-2">
                      <Form.Control
                        type="url"
                        placeholder="https://docs.example.com"
                        value={url}
                        onChange={(e) => handleUrlChange(index, e.target.value)}
                      />
                      <Button
                        variant="outline-danger"
                        onClick={() => removeUrl(index)}
                        className="px-3"
                      >
                        <X size={20} />
                      </Button>
                    </div>
                  ))}
                  <Button
                    variant="outline-primary"
                    className="d-flex align-items-center gap-2 mt-2"
                    onClick={addUrlField}
                    type="button"
                  >
                    <Plus size={20} />
                    Add Another URL
                  </Button>
                </div>
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
                  className="py-3"
                >
                  {isLoading ? (
                    <>
                      <Spinner size="sm" className="me-2" />
                      Updating Assistant...
                    </>
                  ) : (
                    'Update Assistant'
                  )}
                </Button>
              </div>
            </>
          )}
        </Form>
      </Card.Body>
    </Card>
  );
};

export default BotEditor; 