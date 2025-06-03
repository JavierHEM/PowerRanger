import React from "react";
import { Link } from "react-router-dom";
import { Box, Typography, Button, Paper } from "@mui/material";
import "./Home.css";

const Home: React.FC = () => {
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
          maxWidth: 600,
          width: "100%",
          padding: 8,
          textAlign: "center",
          borderRadius: 4,
          background: "rgba(255,255,255,0.97)",
        }}
      >
        <Typography
          variant="h2"
          component="h1"
          gutterBottom
          className="inacap-title"
          sx={{ fontWeight: 800 }}
        >
          DTP INACAP
        </Typography>
        <Typography
          variant="h5"
          className="inacap-subtitle"
          sx={{ mb: 4 }}
        >
          Plataforma de gestión de estudiantes, entrevistas y ajustes razonables.
        </Typography>
        <Button
          variant="contained"
          component={Link}
          to="/login"
          className="inacap-btn"
        >
          Iniciar sesión
        </Button>
      </Paper>
    </Box>
  );
};

export default Home;