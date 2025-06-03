import React, { useState } from "react";
import { Box, Paper, Typography, TextField, Button, Alert } from "@mui/material";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Home.css";

const API_URL = "http://localhost:8000/api/v1/auth/register";

const Register: React.FC = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
    nombres: "",
    apellidos: "",
    rut: "",
    cargo: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const response = await axios.post(API_URL, form);
      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "No se pudo registrar el usuario. Intenta con otro correo o revisa los datos."
      );
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
          Crear usuario
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Correo"
            name="email"
            type="email"
            variant="outlined"
            fullWidth
            required
            margin="normal"
            value={form.email}
            onChange={handleChange}
          />
          <TextField
            label="Contraseña"
            name="password"
            type="password"
            variant="outlined"
            fullWidth
            required
            margin="normal"
            value={form.password}
            onChange={handleChange}
          />
          <TextField
            label="Nombres"
            name="nombres"
            variant="outlined"
            fullWidth
            required
            margin="normal"
            value={form.nombres}
            onChange={handleChange}
          />
          <TextField
            label="Apellidos"
            name="apellidos"
            variant="outlined"
            fullWidth
            required
            margin="normal"
            value={form.apellidos}
            onChange={handleChange}
          />
          <TextField
            label="RUT"
            name="rut"
            variant="outlined"
            fullWidth
            required
            margin="normal"
            value={form.rut}
            onChange={handleChange}
          />
          <TextField
            label="Cargo"
            name="cargo"
            variant="outlined"
            fullWidth
            margin="normal"
            value={form.cargo}
            onChange={handleChange}
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
            Registrar
          </Button>
        </form>
      </Paper>
    </Box>
  );
};

export default Register;