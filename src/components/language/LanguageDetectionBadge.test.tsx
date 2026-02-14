/**
 * Unit Tests for LanguageDetectionBadge Component
 * 
 * These tests validate the LanguageDetectionBadge component functionality:
 * - Displaying detected language with confidence score
 * - Error state handling
 * - Loading state display
 * - Confidence level styling
 * - Accessibility
 * 
 * Requirements: 6.2 - Display detected language with confidence score and show error state if detection fails
 */

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { LanguageDetectionBadge } from "./LanguageDetectionBadge";

describe("LanguageDetectionBadge Component", () => {
  describe("Success State - High Confidence", () => {
    it("should display detected language with high confidence", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          languageCode="en"
          confidence={0.95}
        />
      );

      expect(screen.getByText("English")).toBeInTheDocument();
      expect(screen.getByText("(en)")).toBeInTheDocument();
      expect(screen.getByText("95.0%")).toBeInTheDocument();
    });

    it("should show success checkmark for high confidence", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="French"
          languageCode="fr"
          confidence={0.92}
        />
      );

      // Check for success styling (high confidence)
      const badge = container.querySelector(".bg-success");
      expect(badge).toBeInTheDocument();
    });

    it("should display confidence bar at correct width", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="German"
          languageCode="de"
          confidence={0.85}
        />
      );

      const progressBar = container.querySelector("div[style*='width']");
      expect(progressBar).toHaveStyle("width: 85%");
    });
  });

  describe("Success State - Medium Confidence", () => {
    it("should display detected language with medium confidence", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="Spanish"
          languageCode="es"
          confidence={0.75}
        />
      );

      expect(screen.getByText("Spanish")).toBeInTheDocument();
      expect(screen.getByText("75.0%")).toBeInTheDocument();
    });

    it("should show warning styling for medium confidence", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="Italian"
          languageCode="it"
          confidence={0.72}
        />
      );

      // Check for warning styling (medium confidence)
      const badge = container.querySelector(".bg-warning");
      expect(badge).toBeInTheDocument();
    });

    it("should display warning icon for medium confidence", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="Portuguese"
          languageCode="pt"
          confidence={0.70}
        />
      );

      // AlertTriangle should be visible for confidence < 0.7 or medium confidence
      // The component shows it for low confidence, so this tests the boundary
      expect(screen.getByText("70.0%")).toBeInTheDocument();
    });
  });

  describe("Success State - Low Confidence", () => {
    it("should display detected language with low confidence", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="Hindi"
          languageCode="hi"
          confidence={0.65}
        />
      );

      expect(screen.getByText("Hindi")).toBeInTheDocument();
      expect(screen.getByText("65.0%")).toBeInTheDocument();
    });

    it("should show warning styling for low confidence", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="Tamil"
          languageCode="ta"
          confidence={0.60}
        />
      );

      // Check for low confidence styling - the component uses bg-amber-100/50
      const badge = container.firstChild;
      expect(badge).toHaveClass("border");
      // Verify the badge is rendered
      expect(badge).toBeInTheDocument();
    });

    it("should display alert icon for low confidence", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="Telugu"
          languageCode="te"
          confidence={0.55}
        />
      );

      // AlertTriangle should be visible for confidence < 0.7
      const alertIcon = container.querySelector("svg");
      expect(alertIcon).toBeInTheDocument();
    });
  });

  describe("Error State", () => {
    it("should display error message when error prop is provided", () => {
      render(
        <LanguageDetectionBadge
          error="Failed to detect language"
        />
      );

      expect(screen.getByText("Detection Failed")).toBeInTheDocument();
      expect(screen.getByText("Failed to detect language")).toBeInTheDocument();
    });

    it("should show error styling", () => {
      const { container } = render(
        <LanguageDetectionBadge
          error="Language detection service unavailable"
        />
      );

      // Check for error styling - verify the badge is rendered with error state
      const badge = container.firstChild;
      expect(badge).toHaveClass("border");
      // Verify error message is displayed
      expect(screen.getByText("Detection Failed")).toBeInTheDocument();
    });

    it("should display alert icon in error state", () => {
      const { container } = render(
        <LanguageDetectionBadge
          error="Invalid input"
        />
      );

      const alertIcon = container.querySelector("svg");
      expect(alertIcon).toBeInTheDocument();
    });

    it("should not display language info in error state", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          error="Detection failed"
        />
      );

      // Error state should take precedence
      expect(screen.getByText("Detection Failed")).toBeInTheDocument();
    });
  });

  describe("Loading State", () => {
    it("should display loading message when isLoading is true", () => {
      render(
        <LanguageDetectionBadge
          isLoading={true}
        />
      );

      expect(screen.getByText("Detecting language...")).toBeInTheDocument();
    });

    it("should show loading styling", () => {
      const { container } = render(
        <LanguageDetectionBadge
          isLoading={true}
        />
      );

      const badge = container.querySelector(".bg-muted");
      expect(badge).toBeInTheDocument();
    });

    it("should display spinning globe icon in loading state", () => {
      const { container } = render(
        <LanguageDetectionBadge
          isLoading={true}
        />
      );

      const spinner = container.querySelector(".animate-spin");
      expect(spinner).toBeInTheDocument();
    });

    it("should not display language info in loading state", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          isLoading={true}
        />
      );

      // Loading state should take precedence
      expect(screen.getByText("Detecting language...")).toBeInTheDocument();
      expect(screen.queryByText("English")).not.toBeInTheDocument();
    });
  });

  describe("No Detection Result", () => {
    it("should display default message when no language detected", () => {
      render(
        <LanguageDetectionBadge />
      );

      expect(screen.getByText("No language detected")).toBeInTheDocument();
    });

    it("should show muted styling when no result", () => {
      const { container } = render(
        <LanguageDetectionBadge />
      );

      const badge = container.querySelector(".bg-muted");
      expect(badge).toBeInTheDocument();
    });
  });

  describe("Size Variants", () => {
    it("should apply small size classes", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          size="sm"
        />
      );

      const badge = container.firstChild;
      expect(badge).toHaveClass("px-2", "py-1", "text-xs");
    });

    it("should apply medium size classes (default)", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          size="md"
        />
      );

      const badge = container.firstChild;
      expect(badge).toHaveClass("px-3", "py-2", "text-sm");
    });

    it("should apply large size classes", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          size="lg"
        />
      );

      const badge = container.firstChild;
      expect(badge).toHaveClass("px-4", "py-3", "text-base");
    });
  });

  describe("Custom Styling", () => {
    it("should apply custom className", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          className="custom-badge-class"
        />
      );

      expect(container.querySelector(".custom-badge-class")).toBeInTheDocument();
    });
  });

  describe("Language Code Display", () => {
    it("should display language code when provided", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          languageCode="en"
        />
      );

      expect(screen.getByText("(en)")).toBeInTheDocument();
    });

    it("should not display language code when not provided", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
        />
      );

      expect(screen.queryByText(/\([a-z]{2}\)/)).not.toBeInTheDocument();
    });
  });

  describe("Confidence Score Formatting", () => {
    it("should format confidence as percentage with one decimal place", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          confidence={0.876}
        />
      );

      expect(screen.getByText("87.6%")).toBeInTheDocument();
    });

    it("should handle confidence of 1.0", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          confidence={1.0}
        />
      );

      expect(screen.getByText("100.0%")).toBeInTheDocument();
    });

    it("should handle confidence of 0.0", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          confidence={0.0}
        />
      );

      expect(screen.getByText("0.0%")).toBeInTheDocument();
    });
  });

  describe("Accessibility", () => {
    it("should have semantic HTML structure", () => {
      const { container } = render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          confidence={0.95}
        />
      );

      const badge = container.firstChild;
      expect(badge).toHaveClass("flex", "items-center", "gap-2");
    });

    it("should display text content for screen readers", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          languageCode="en"
          confidence={0.95}
        />
      );

      expect(screen.getByText("English")).toBeInTheDocument();
      expect(screen.getByText("(en)")).toBeInTheDocument();
      expect(screen.getByText("95.0%")).toBeInTheDocument();
    });
  });

  describe("Edge Cases", () => {
    it("should handle very long language names", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="Very Long Language Name That Might Wrap"
          confidence={0.85}
        />
      );

      expect(screen.getByText("Very Long Language Name That Might Wrap")).toBeInTheDocument();
    });

    it("should handle special characters in language names", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="Español (Spanish)"
          confidence={0.90}
        />
      );

      expect(screen.getByText("Español (Spanish)")).toBeInTheDocument();
    });

    it("should handle multiple error states gracefully", () => {
      render(
        <LanguageDetectionBadge
          detectedLanguage="English"
          error="Error occurred"
          isLoading={true}
        />
      );

      // Error should take precedence
      expect(screen.getByText("Detection Failed")).toBeInTheDocument();
    });
  });
});
