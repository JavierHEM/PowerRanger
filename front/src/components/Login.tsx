import React, { useState } from "react";
import { Box, Paper, Typography, TextField, Button, Alert } from "@mui/material";
import axios from "axios";
import { Link } from "react-router-dom";
import "./Home.css"; // Reutilizamos los estilos

const API_URL = "http://localhost:8000/api/v1/auth/login"; // Cambia si tu backend usa otro puerto

const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const response = await axios.post(API_URL, {
        username: email,
        password: password,
      });
      localStorage.setItem("token", response.data.access_token);
      window.location.href = "/dashboard";
    } catch (err) {
      setError("Credenciales incorrectas o error de conexión.");
    }
  };

  return (
    <Box
      className="home-bg"
      sx={{
        minHeight: "100vh",
        width: "100vw",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Paper
        elevation={10}
        className="inacap-shadow"
        sx={{
          maxWidth: 400,
          width: "100%",
          padding: 6,
          textAlign: "center",
          borderRadius: 4,
          background: "rgba(255,255,255,0.97)",
        }}
      >
        <Typography
          variant="h4"
          className="inacap-title"
          sx={{ fontWeight: 800, mb: 2 }}
        >
          Iniciar sesión
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Correo"
            type="email"
            variant="outlined"
            fullWidth
            required
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            label="Contraseña"
            type="password"
            variant="outlined"
            fullWidth
            required
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && (
            <Alert severity="error" sx={{ mt: 2, mb: 1 }}>
              {error}
            </Alert>
          )}
          <Button
            type="submit"
            variant="contained"
            className="inacap-btn"
            fullWidth
            sx={{ mt: 2 }}
          >
            Entrar
          </Button>
          <Button
            component={Link}
            to="/register"
            variant="outlined"
            fullWidth
            sx={{ mt: 2 }}
          >
            Crear usuario
          </Button>
        </form>
      </Paper>
    </Box>
  );
};

export default Login;