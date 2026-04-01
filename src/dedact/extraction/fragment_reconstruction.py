"""
Fragment Reconstruction Module
Reconstruct text from partial fragments using language models and context
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
import re


@dataclass
class ReconstructionCandidate:
    """Possible reconstruction of fragment"""
    reconstructed_text: str
    confidence: float
    method: str
    reasoning: str


class FragmentReconstructor:
    """
    Reconstruct text from partial fragments
    
    Methods:
    - Dictionary-based: Complete partial words
    - Language model: Predict missing words
    - Context-aware: Use document vocabulary
    """
    
    def __init__(self, max_candidates: int = 5):
        """
        Initialize fragment reconstructor
        
        Args:
            max_candidates: Maximum reconstruction candidates to return
        """
        self.max_candidates = max_candidates
        self.method_name = 'fragment_reconstruction'
        
        # Simple English word list (real implementation would use full dictionary)
        self.common_words = set([
            'the', 'and', 'for', 'are', 'was', 'were', 'been',
            'have', 'has', 'had', 'will', 'would', 'could', 'should',
            'person', 'people', 'company', 'companies', 'payment', 'contract',
            'agreement', 'date', 'time', 'year', 'month', 'day'
        ])
    
    def reconstruct(
        self,
        fragment: str,
        context: Optional[str] = None,
        document_vocabulary: Optional[set] = None
    ) -> List[ReconstructionCandidate]:
        """
        Reconstruct text from fragment
        
        Args:
            fragment: Partial text fragment
            context: Surrounding text for context
            document_vocabulary: Set of words used in document
            
        Returns:
            List of reconstruction candidates
        """
        candidates = []
        
        # Determine fragment type
        if '_' in fragment or '*' in fragment:
            # Partial word (e.g., "extr_ction")
            candidates.extend(self._reconstruct_partial_word(fragment, document_vocabulary))
        elif '[' in fragment and ']' in fragment:
            # Missing word gap (e.g., "The [GAP] went")
            candidates.extend(self._reconstruct_missing_word(fragment, context))
        else:
            # General fragment
            candidates.extend(self._reconstruct_general_fragment(fragment, context))
        
        # Sort by confidence and return top N
        candidates.sort(key=lambda c: c.confidence, reverse=True)
        return candidates[:self.max_candidates]
    
    def _reconstruct_partial_word(
        self,
        fragment: str,
        document_vocabulary: Optional[set]
    ) -> List[ReconstructionCandidate]:
        """
        Complete partial words
        
        Args:
            fragment: Partial word with wildcards
            document_vocabulary: Document-specific vocabulary
            
        Returns:
            List of candidates
        """
        candidates = []
        
        # Convert to regex pattern
        pattern = fragment.replace('_', '.').replace('*', '.*')
        regex = re.compile(pattern, re.IGNORECASE)
        
        # Check document vocabulary first (highest confidence)
        if document_vocabulary:
            matches = [word for word in document_vocabulary if regex.match(word)]
            for match in matches:
                candidates.append(ReconstructionCandidate(
                    reconstructed_text=match,
                    confidence=0.85,  # High confidence from document context
                    method='document_vocabulary',
                    reasoning=f"Found in document vocabulary, matches pattern '{fragment}'"
                ))
        
        # Check common words (medium confidence)
        common_matches = [word for word in self.common_words if regex.match(word)]
        for match in common_matches:
            if match not in [c.reconstructed_text for c in candidates]:
                candidates.append(ReconstructionCandidate(
                    reconstructed_text=match,
                    confidence=0.65,
                    method='common_dictionary',
                    reasoning=f"Common word matching pattern '{fragment}'"
                ))
        
        # Adjust confidence based on specificity
        for candidate in candidates:
            specificity = len(fragment.replace('_', '').replace('*', '')) / len(candidate.reconstructed_text)
            candidate.confidence *= (0.5 + specificity * 0.5)
        
        return candidates
    
    def _reconstruct_missing_word(
        self,
        fragment: str,
        context: Optional[str]
    ) -> List[ReconstructionCandidate]:
        """
        Predict missing words from context
        
        Args:
            fragment: Text with [GAP] marker
            context: Surrounding text
            
        Returns:
            List of candidates
        """
        candidates = []
        
        # Extract before and after text
        parts = fragment.split('[GAP]')
        if len(parts) != 2:
            return candidates
        
        before = parts[0].strip().split()[-3:] if parts[0] else []  # Last 3 words
        after = parts[1].strip().split()[:3] if parts[1] else []  # Next 3 words
        
        # Simple pattern matching (real implementation would use language model)
        if before and after:
            # Pattern: "The [GAP] went"
            if before[-1].lower() == 'the':
                # Likely noun
                predictions = ['person', 'man', 'woman', 'company', 'group', 'team']
                for pred in predictions:
                    candidates.append(ReconstructionCandidate(
                        reconstructed_text=pred,
                        confidence=0.55,
                        method='pattern_matching',
                        reasoning=f"Noun follows article 'the'"
                    ))
            elif after and after[0].lower() in ('is', 'was', 'are', 'were'):
                # Subject position
                predictions = ['it', 'he', 'she', 'this', 'that']
                for pred in predictions:
                    candidates.append(ReconstructionCandidate(
                        reconstructed_text=pred,
                        confidence=0.50,
                        method='grammar_rules',
                        reasoning=f"Subject before verb '{after[0]}'"
                    ))
        
        return candidates
    
    def _reconstruct_general_fragment(
        self,
        fragment: str,
        context: Optional[str]
    ) -> List[ReconstructionCandidate]:
        """
        Reconstruct general text fragments
        
        Args:
            fragment: Text fragment
            context: Context text
            
        Returns:
            List of candidates
        """
        candidates = []
        
        # Check if fragment is a single incomplete word
        if len(fragment.split()) == 1 and len(fragment) >= 3:
            # Try to find similar words in context
            if context:
                context_words = set(re.findall(r'\b\w+\b', context.lower()))
                
                # Find words starting with fragment
                similar = [
                    word for word in context_words
                    if word.startswith(fragment.lower()) and len(word) > len(fragment)
                ]
                
                for word in similar:
                    candidates.append(ReconstructionCandidate(
                        reconstructed_text=word,
                        confidence=0.70,
                        method='context_completion',
                        reasoning=f"Found similar word '{word}' in context"
                    ))
        
        # If no candidates found, return fragment as-is with low confidence
        if not candidates:
            candidates.append(ReconstructionCandidate(
                reconstructed_text=fragment,
                confidence=0.20,
                method='no_reconstruction',
                reasoning="Could not reconstruct fragment"
            ))
        
        return candidates
    
    def build_document_vocabulary(self, full_text: str) -> set:
        """
        Build vocabulary from document text
        
        Args:
            full_text: Complete document text
            
        Returns:
            Set of unique words
        """
        # Extract words (alphanumeric + basic punctuation)
        words = re.findall(r'\b[a-zA-Z]{2,}\b', full_text.lower())
        return set(words)
    
    def score_reconstruction_quality(
        self,
        original_fragment: str,
        reconstructed: str,
        context: Optional[str] = None
    ) -> float:
        """
        Score quality of reconstruction
        
        Args:
            original_fragment: Original fragment
            reconstructed: Reconstructed text
            context: Context text
            
        Returns:
            Quality score (0.0-1.0)
        """
        score = 0.5  # Base score
        
        # Length similarity
        if len(reconstructed) >= len(original_fragment):
            score += 0.2
        
        # Character overlap
        common_chars = set(original_fragment.lower()) & set(reconstructed.lower())
        overlap_ratio = len(common_chars) / len(set(original_fragment.lower())) if original_fragment else 0
        score += overlap_ratio * 0.3
        
        # Context validation (if available)
        if context and reconstructed.lower() in context.lower():
            score += 0.2
        
        return min(1.0, score)
    
    def batch_reconstruct(
        self,
        fragments: List[str],
        context: Optional[str] = None,
        document_vocabulary: Optional[set] = None
    ) -> Dict[str, List[ReconstructionCandidate]]:
        """
        Reconstruct multiple fragments
        
        Args:
            fragments: List of text fragments
            context: Shared context
            document_vocabulary: Document vocabulary
            
        Returns:
            Dictionary mapping fragments to candidates
        """
        results = {}
        
        for fragment in fragments:
            results[fragment] = self.reconstruct(
                fragment,
                context,
                document_vocabulary
            )
        
        return results
