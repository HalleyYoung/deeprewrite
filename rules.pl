use_module(library(clpfd)).
use_module(library(chr)).


%Unification
unify(T1, T2), def(T1, A) ==> def(T2, A).
unify(T1, T2), def(T2, A) => def(T1, A).
unify(T1, T2), def(T1, A), def(T2, B), A != B ==> fail.
def(T1, A), def(T2, A) <=> unify(T1, T2).

%succeeds
succeeds([X | XS]) ==> succeeds(X,XS).
succeeds(X,Y), succeeds(Y,Z) <=> succeeds(X,Z).
def(T1, A), def(T2, B), A > B, succeeds(T1, T2) ==> fail.

%List of defined

% Defining parts of a sonata
%Sonata((t1,t1_def), (t2, t2_def)), defs([X | Ys]) ==> Primary((t1,t1_def), (X + 1, false)), Secondary((X + 1,false), (t2, t2_def)), defs([X + 1, X | Ys])
% Defining relationship between P, TR, and S
    % P and S are both somewhat similar to TR, but different from each other
    % TR is more restless than S
    % TR modulates to key x != key of P, S is in key x
% Development modulates a lot, contains material from P and material from S
% Recapitulation in same key as P, first close to P then close to S


%Defining period
period((t1, t2)), vars([X | Ys]) ==> succeeds([t1, X + 1, X + 2, X + 3, t2]), distance((t1, X + 1), (X + 1, t2), i(1,3)), distance((t1, X + 1), (X + 2, X + 3), i(1,3)), cadence(X + 2, i(1,2)), cadence(t2, i(3,4)), undef([X + 1, X + 2, X + 3]), vars([X + 3, X + 2, X + 1, X | Ys]).
period((t1,t2)), vars([X | Ys], classical(t1, t2), def(t1, A), def(t2, B) ==> succeeds([t1, X + 1, X + 2, X + 3, t2]), distance((t1, X + 1), (X + 1, t2), i(1,3)), distance((t1, X + 1), (X + 2, X + 3), i(1,3)), halfCadence(X + 1), authenticCadence(t2), def(X + 1, A + (B - A)/4), def(X + 2, A + 2*(B - A)/4), def(X+3, A+3*(B - A)/4), vars([X + 3, X + 2, X + 1, X | Ys]).
%Defining sentence


% Defining properties of Hindustani music
    % Either unmetered or additive rhythm
    % Fixed raga with ornamentations on certain notes?
    % Non-diatonic scales
    % Tanbura drone
    % Tabla establishing additive rhythm


% Defining meter
    % Defining additive rhythm
    additiveRhythmTot(T1,T2), allInstrs(Instr_list) ==> additiveRhythm(T1,T2, Instr_list). 
    additiveRhythm(T1, T2, Instr_list) ==> strongMeter(T1,T2, Instr_list), additiveMeter(T1,T2, Instr_list, X).
    additiveRhythm(T1,T2, Instr_list), divisiveRhythm(T1,T2,Instr_list) ==> fail.
        % Rarely go between beats of 3+2+2
    % Metric = sum(strong beats) + context
    % Meter in form of (start_offset, [tactus, beat])
    % genMeter
    additiveMeter(T1,T2,Instr_list, X) ==> additiveBeat(T1,T2,Instr_list, X).
    additiveMeter(T1,T2,Instr_list, X) ==> additiveTactus(T1,T2,Instr_list, X).
    additiveMeter(T1,T2,Instr_list, X), additiveMeter(T1, T2, Instr_list, Y), Y != X ==> fail.

    meterLen(T1,T2,Instr_list, N), additiveBeat(T1,T2,Instr_list), def(T1, A), def(T2, B) ==> meters(T1,T2,Instr_List,X), genAddMetersBeat(N,B - A,X), hasMeters(T1,T2, Instr_list, X).
    meterLen(T1,T2,Instr_list, N), additiveTactus(T1,T2,Instr_list), def(T1, A), def(T2, B) ==> meters(T1,T2,Instr_List,X), genAddMetersTactus(N,B - A,X), hasMeters(T1,T2, Instr_list, X).

    % Strong beats = (strong one on first down) + (more strong 1’s on other downbeats) + (some credit for half downbeats)
    strongMeter(T1,T2, Instr_list), def(T1, A), def(T2, B), B > A + 20 ==> meterLen(T1,T2, InstrList, 1).
    strongMeter(T1,T2, Instr_list), def(T1, A), def(T2, B), B < A + 10 ==> meterLen(T1, T2, InstrList, 1), sync(T1,T2, InstrList, i(0,2)).



    %genMeter
    genAddMetersBeat(1, TimeLen, (Offset, Beats)) :- getOffBeats(Offset, Beats, TimeLen). 
    genAddMetersBeat(N, TimeLen, X | XS) :- genAddMetersBeat(1, TimeLen, X), genAddMetersBeat(N - 1, TimeLen, XS).
    getOffBeat(Offset, [A,B], TimeLen) :- (TimeLen - Offset) mod (A + B) #= 0.
    getOffBeat(Offset, [A,B,C], TimeLen) :- (TimeLen - Offset) mod (A + B + C) #= 0.


% Defining syncopation relative to meter
sync(T1,T2, InstrList, i(Sync_A,Sync_B)), def(T1,K), def(T2, L), meters(T1,T2,InstrList, Meters), rhythmicDensity(T1,T2,InstrList, i(Dens_A,Dens_B)), nRhyth(InstrList, 1) ==> hasRhythm(T1,T2, InstrList, X), getRhythmFromSyncDensMeterLen(Sync_A, Sync_B, Dens_A, Dens_B, Meters, L - K). 

tactusPerBeat(60).

%rhythm definition
getRhythmFromSyncDensMeterLen(Sync_A, Sync_B, Dens_A, Dens_B, (Offset, Meters), Tactus, TotLength, Rhy) :- HasStrongPattern(Offset, Meters, Tactus, TotLength, X), hasStrengthOnPattern(X, Rhy).

% Defining properties of classical music
   % strong tonal center/function
   classical(T1,T2) ==> isTonal(T1, T2), hasStrongDivisiveMeter(T1,T2).

   % strong metric coherence
   % strong tonal cadences

% Defining punctuation

% Defining using scale
    % Diatonic scale
    diatonic(Scale) :- possibleRotation(Scale, 12, [0,2,4,5,7,9,11]).
    possibleRotation(Scale, 0, Scale).
    possibleRotation(Scale, N, Scale2) :- N #> 0, possibleRotation(Scale, N - 1, Scale2).
    possibleRotation(Scale, N, Scale2) :- map2(plusMod12, N, Scale, Scale2).

    % Modal scale


% Defining using chord


% Defining tension
    increased_tension(T1,T2), vars(X | XS) ==> succeeds([T1, X + 1, X + 2, X + 3, T2]), tension(T1, X + 1, Ten1), tension(X + 1, X + 2, Ten2), tension(X + 2, X + 3, Ten3), tension(X+3, T2, Ten4), inRange(Ten4, [7,10]), inRange(Ten1, [0,2]), Ten4 > Ten3, Ten3 > Ten2, Ten2 > Ten1.
    % Acceleration
    % Harmonic rhythm


% Defining tonal function





% Defining counterpoint
    %  No dissonance not resolving to consonance?
    % Definition of suspension/anticipation
    % Definition of adjacent rhythms


% Defining typicality
    % Number of direction changes
    % Number of leaps
    % Number of different intervals
    % Number of different durations
    % Fit with meter


% Defining distance
    % Part/whole subdivisions
    % Melody only similarity required
    % Accompaniment/Melody division
    % Similarity at lower ontological level
        % Abstraction levels of ontological levels
            % Notes
                % Pitches
                    % Intervals
                    % Chords
                    % Scales
                    % Contour
                % Rhythms
                % Instruments                
    % Similarity for specific transformations
        % Notes
        % Intervals
        % Chords
        % Scales
        % Contour
        % Rhythm
        % Syncopation
        % Meter
        % Rhythmic Density
        % Polyrhythm
        % Smallest subdivision
        % Rhythmic contour


% Defining accompaniment
    % In relationship to meter
    % Types
        % Alberti bass
        % Pedal
        % Chords
        % Stride


% Defining types of textures
    % Melody-accompaniment
    % Melody-countermelody-accompaniment